from flask import render_template, redirect, url_for, flash, request, current_app
from . import produccion
from app.extensions import db, mongo_fotos
from app.models import (
    SolicitudProduccion, SolicitudProduccionDetalle,
    Lote, CanalCorte, Canal, Corte, Categoria,
    Producto, Receta,
)
from flask_login import login_required, current_user
from flask_security import roles_required
from datetime import datetime, date



# ═════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _foto_b64_de(id_foto):
    """Foto desde MongoDB en base64."""
    if not id_foto or mongo_fotos is None:
        return None
    try:
        doc = mongo_fotos.find_one({'idFoto': str(id_foto)})
        if doc and doc.get('foto'):
            raw = doc['foto']
            if not raw.startswith('data:'):
                raw = f'data:image/jpeg;base64,{raw}'
            return raw
    except Exception:
        pass
    return None


def _generar_numero_lote_produccion():
    """Numero de lote para Lote producido por corte.
    Formato: LP-MesDDNN  (ej: LP-Abr0901)."""
    meses_corto = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',
                   7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
    hoy = date.today()
    prefijo = f"LP-{meses_corto[hoy.month]}{hoy.day:02d}"
    ultimo = (
        Lote.query
        .filter(Lote.numeroLote.like(f"{prefijo}%"))
        .order_by(Lote.numeroLote.desc())
        .first()
    )
    if ultimo and ultimo.numeroLote:
        try:
            ultimo_num = int(ultimo.numeroLote[len(prefijo):])
        except (ValueError, IndexError):
            ultimo_num = 0
    else:
        ultimo_num = 0
    return f"{prefijo}{ultimo_num + 1:02d}"


# ═════════════════════════════════════════════════════════════════════════════
#  LISTADO — solicitudes pendientes de completar
# ═════════════════════════════════════════════════════════════════════════════

@produccion.route('/produccion')
@login_required
@roles_required('admin')
def index():
    pendientes = (
        SolicitudProduccion.query
        .filter(SolicitudProduccion.estatus == 'Pendiente')
        .order_by(SolicitudProduccion.fechaSolicitud.asc())
        .all()
    )

    completadas = (
        SolicitudProduccion.query
        .filter(SolicitudProduccion.estatus == 'Completada')
        .order_by(SolicitudProduccion.fechaCompletada.desc())
        .limit(20)
        .all()
    )

    # Enriquecer pendientes con datos segun tipo
    items_pendientes = []
    for sol in pendientes:
        detalle = sol.detalles.first()

        if sol.tipoReceta == 'Corte':
            cc = CanalCorte.query.get(detalle.idCanalCorte) if detalle and detalle.idCanalCorte else None
            corte = Corte.query.get(cc.idCorte) if cc else (sol.corte if sol.corte else None)
            canal = Canal.query.get(cc.idCanal) if cc else None
            cat = corte.categoria if corte and corte.categoria else None
            items_pendientes.append({
                'solicitud':        sol,
                'tipo':             'Corte',
                'nombre':           corte.nombreCorte if corte else '—',
                'categoria':        cat.nombreCategoria if cat else '—',
                'canal_id':         canal.idCanal if canal else '—',
                'canal_peso':       canal.Peso if canal else '—',
                'cantidad_esperada': cc.CantidadEsperada if cc else '—',
                'foto_b64':         _foto_b64_de(corte.idFoto) if corte else None,
                'usuario':          sol.usuario.email if sol.usuario else '—',
            })
        else:  # Personalizada
            receta_obj = sol.receta
            producto = receta_obj.producto if receta_obj else None
            foto = _foto_b64_de(receta_obj.idFoto) if receta_obj else None
            items_pendientes.append({
                'solicitud':        sol,
                'tipo':             'Personalizada',
                'nombre':           sol.nombreReceta,
                'categoria':        '—',
                'canal_id':         '—',
                'canal_peso':       '—',
                'cantidad_esperada': f'{sol.cantidadProducir} uds',
                'foto_b64':         foto,
                'usuario':          sol.usuario.email if sol.usuario else '—',
            })

    # Enriquecer completadas
    items_completadas = []
    for sol in completadas:
        detalle = sol.detalles.first()
        lote_prod = Lote.query.get(detalle.idLoteProducido) if detalle and detalle.idLoteProducido else None

        if sol.tipoReceta == 'Corte':
            cc = CanalCorte.query.get(detalle.idCanalCorte) if detalle and detalle.idCanalCorte else None
            merma = cc.Merma if cc else 0
        else:
            # Personalizada: la merma no aplica (se consume lo exacto de la receta)
            merma = None

        items_completadas.append({
            'solicitud':     sol,
            'tipo':          sol.tipoReceta or 'Corte',
            'nombre':        sol.nombreReceta,
            'lote_numero':   lote_prod.numeroLote if lote_prod else '—',
            'kg_producidos': lote_prod.totalMateria if lote_prod else 0,
            'merma':         merma,
            'usuario':       sol.usuario.email if sol.usuario else '—',
        })

    return render_template(
        'admin/produccion/produccion.html',
        items_pendientes=items_pendientes,
        items_completadas=items_completadas,
        total_pendientes=len(items_pendientes),
        total_completadas=len(items_completadas),
    )


# ═════════════════════════════════════════════════════════════════════════════
#  COMPLETAR — formulario para dar peso obtenido y concretar
# ═════════════════════════════════════════════════════════════════════════════

@produccion.route('/produccion/<int:id>/completar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def completar(id):
    sol = SolicitudProduccion.query.get_or_404(id)

    if sol.estatus != 'Pendiente':
        flash('Esta solicitud ya fue completada o cancelada.', 'warning')
        return redirect(url_for('produccion.index'))

    # Despachar segun tipo
    if sol.tipoReceta == 'Personalizada':
        return _completar_personalizada(sol)
    return _completar_corte(sol)


# ── Completar tipo Corte ─────────────────────────────────────────────────────
def _completar_corte(sol):
    detalle = sol.detalles.first()
    cc = CanalCorte.query.get(detalle.idCanalCorte) if detalle and detalle.idCanalCorte else None
    corte = Corte.query.get(cc.idCorte) if cc else (sol.corte if sol.corte else None)
    canal = Canal.query.get(cc.idCanal) if cc else None
    cat = corte.categoria if corte and corte.categoria else None

    info = {
        'corte_nombre':     corte.nombreCorte if corte else '—',
        'categoria':        cat.nombreCategoria if cat else '—',
        'canal_id':         canal.idCanal if canal else '—',
        'canal_peso':       canal.Peso if canal else '—',
        'cantidad_esperada': cc.CantidadEsperada if cc else 0,
        'foto_b64':         _foto_b64_de(corte.idFoto) if corte else None,
        'fecha_sacrificio': canal.fechaSacrificio.strftime('%d/%m/%Y') if (canal and canal.fechaSacrificio) else '—',
    }

    if request.method == 'POST':
        try:
            cantidad_obtenida = float(request.form.get('cantidadObtenida') or 0)
        except (TypeError, ValueError):
            flash('La cantidad obtenida debe ser un numero valido.', 'danger')
            return redirect(url_for('produccion.completar', id=sol.idSolicitud))

        if cantidad_obtenida <= 0:
            flash('La cantidad obtenida debe ser mayor a cero.', 'danger')
            return redirect(url_for('produccion.completar', id=sol.idSolicitud))

        if not cc:
            flash('No se encontro el canal_corte vinculado a esta solicitud.', 'danger')
            return redirect(url_for('produccion.completar', id=sol.idSolicitud))

        try:
            esperada = cc.CantidadEsperada or 0
            merma    = round(esperada - cantidad_obtenida, 3)

            cc.CantidadObtenida = cantidad_obtenida
            cc.Merma            = merma
            cc.estatus          = 'Consumido'

            numero_lote = _generar_numero_lote_produccion()
            fecha_cad_lote = canal.fechaCaducidad if canal else None
            lote_producido = Lote(
                idCanalCorte      = cc.idCanalCorte,
                idMateriaProveida = None,
                idOrdenCompra     = None,
                numeroLote        = numero_lote,
                cantidadDeUnidad  = 1,
                cantidadPorUnidad = cantidad_obtenida,
                totalMateria      = cantidad_obtenida,
                precioPorUnidad   = 0.0,
                totalCosto        = 0.0,
                fechaCaducidad    = fecha_cad_lote,
                estatus           = 'Disponible',
                idUsuario         = current_user.id,
            )
            db.session.add(lote_producido)
            db.session.flush()

            sol.estatus         = 'Completada'
            sol.fechaCompletada = datetime.now()

            if detalle:
                detalle.idLoteProducido   = lote_producido.idLote
                detalle.cantidadConsumida = cantidad_obtenida

            db.session.commit()

            cat_nombre = cat.nombreCategoria if cat else ''
            nombre_corte = f'{corte.nombreCorte} ({cat_nombre})' if (corte and cat_nombre) else (corte.nombreCorte if corte else '—')

            email_usuario = current_user.email if current_user and current_user.is_authenticated else 'sistema'
            current_app.logger.info(
                f"Produccion completada (Corte) | corte={nombre_corte} "
                f"| lote={numero_lote} | obtenido={cantidad_obtenida:g}kg | merma={merma:g}kg "
                f"| solicitud=#{sol.idSolicitud} | autorizo={email_usuario} "
                f"| ip={request.remote_addr}"
            )

            flash(
                f'Produccion completada: "{nombre_corte}". '
                f'Lote {numero_lote} creado con {cantidad_obtenida:g} kg '
                f'(merma: {merma:g} kg).',
                'success'
            )
            return redirect(url_for('produccion.index'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f"Error al completar produccion (Corte) | solicitud=#{sol.idSolicitud} | error={e}"
            )
            flash(f'Error al completar la produccion: {e}', 'danger')
            return redirect(url_for('produccion.completar', id=sol.idSolicitud))

    return render_template(
        'admin/produccion/produccion_completar.html',
        solicitud=sol,
        info=info,
        tipo='Corte',
    )


# ── Completar tipo Personalizada ─────────────────────────────────────────────
def _completar_personalizada(sol):
    receta_obj = sol.receta
    producto   = receta_obj.producto if receta_obj else None
    detalles   = sol.detalles.all()

    # Construir info de ingredientes para el template
    ingredientes_info = []
    for det in detalles:
        lote = Lote.query.get(det.idLote) if det.idLote else None
        mp   = det.materiaPrima
        ingredientes_info.append({
            'nombre':     mp.nombreMateriaPrima if mp else '—',
            'lote':       (lote.numeroLote or f'#{lote.idLote}') if lote else '—',
            'necesario':  det.cantidadConsumida,
            'disponible': lote.totalMateria if lote else 0,
            'lote_ok':    lote and lote.estatus == 'Disponible' and (lote.totalMateria or 0) >= det.cantidadConsumida,
        })

    info = {
        'nombre':           sol.nombreReceta,
        'cantidad_producir': sol.cantidadProducir,
        'foto_b64':         _foto_b64_de(receta_obj.idFoto) if receta_obj else None,
        'ingredientes':     ingredientes_info,
        'producto':         producto.NombreProducto if producto else '—',
    }

    if request.method == 'POST':
        errores = []
        consumos = []

        for det in detalles:
            lote = Lote.query.get(det.idLote) if det.idLote else None
            nombre_ing = det.materiaPrima.nombreMateriaPrima if det.materiaPrima else '—'

            if not lote or lote.estatus != 'Disponible':
                errores.append(f'El lote para "{nombre_ing}" ya no esta disponible.')
                continue

            if (lote.totalMateria or 0) < det.cantidadConsumida:
                errores.append(
                    f'Stock insuficiente en lote {lote.numeroLote or lote.idLote} '
                    f'para "{nombre_ing}". '
                    f'Necesario: {det.cantidadConsumida:g}, disponible: {lote.totalMateria:g}.'
                )
                continue

            consumos.append((det, lote))

        if errores:
            for e in errores:
                flash(e, 'danger')
            return redirect(url_for('produccion.completar', id=sol.idSolicitud))

        try:
            # Consumir stock de cada lote y calcular totales
            total_consumido = 0
            fecha_cad_proxima = None
            for det, lote in consumos:
                total_consumido += det.cantidadConsumida
                lote.totalMateria = (lote.totalMateria or 0) - det.cantidadConsumida
                if lote.totalMateria <= 0:
                    lote.totalMateria = 0
                    lote.estatus      = 'Agotado'
                # Fecha de caducidad mas proxima de los lotes consumidos
                if lote.fechaCaducidad:
                    if fecha_cad_proxima is None or lote.fechaCaducidad < fecha_cad_proxima:
                        fecha_cad_proxima = lote.fechaCaducidad

            total_consumido = round(total_consumido, 3)

            # Crear lote de produccion para trazabilidad
            numero_lote = _generar_numero_lote_produccion()
            lote_producido = Lote(
                idCanalCorte      = None,
                idMateriaProveida = None,
                idOrdenCompra     = None,
                numeroLote        = numero_lote,
                cantidadDeUnidad  = sol.cantidadProducir,
                cantidadPorUnidad = round(total_consumido / sol.cantidadProducir, 3) if sol.cantidadProducir else total_consumido,
                totalMateria      = total_consumido,
                precioPorUnidad   = 0.0,
                totalCosto        = 0.0,
                fechaCaducidad    = fecha_cad_proxima,
                estatus           = 'Disponible',
                idUsuario         = current_user.id,
            )
            db.session.add(lote_producido)
            db.session.flush()

            # Vincular todos los detalles al lote producido
            for det, _ in consumos:
                det.idLoteProducido = lote_producido.idLote

            # Incrementar stock del producto
            if producto is not None:
                producto.StockProducto = (producto.StockProducto or 0) + sol.cantidadProducir

            sol.estatus         = 'Completada'
            sol.fechaCompletada = datetime.now()

            db.session.commit()

            email_usuario = current_user.email if current_user and current_user.is_authenticated else 'sistema'
            current_app.logger.info(
                f"Produccion autorizada (Personalizada) | receta={sol.nombreReceta} "
                f"| cantidad={sol.cantidadProducir} uds | lote={numero_lote} "
                f"| consumido={total_consumido:g}kg "
                f"| producto={producto.NombreProducto if producto else '—'} "
                f"| solicitud=#{sol.idSolicitud} | autorizo={email_usuario} "
                f"| ip={request.remote_addr}"
            )

            flash(
                f'Produccion autorizada: se produjeron {sol.cantidadProducir} unidad(es) '
                f'de "{sol.nombreReceta}". '
                f'Lote {numero_lote} creado con {total_consumido:g} kg consumidos.',
                'success'
            )
            return redirect(url_for('produccion.index'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f"Error al completar produccion (Personalizada) | solicitud=#{sol.idSolicitud} | error={e}"
            )
            flash(f'Error al completar la produccion: {e}', 'danger')
            return redirect(url_for('produccion.completar', id=sol.idSolicitud))

    return render_template(
        'admin/produccion/produccion_completar.html',
        solicitud=sol,
        info=info,
        tipo='Personalizada',
    )
