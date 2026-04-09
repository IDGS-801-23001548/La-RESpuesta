from flask import render_template, redirect, url_for, flash, request
from . import solicitud_de_produccion
from app.extensions import db, mongo_fotos
from app.models import (
    Receta, RecetaMateriaPrima,
    SolicitudProduccion, SolicitudProduccionDetalle,
    MateriaPrima, MateriaProveida, Lote,
    Producto,
    Canal, CanalCorte, Corte, Categoria,
)
from flask_login import login_required, current_user
from flask_security import roles_required
from datetime import datetime, date


# ═════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _foto_b64_de(id_foto):
    """Devuelve la foto en base64 desde MongoDB para mostrarla en templates."""
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


def _lotes_disponibles_query():
    """Lotes con estatus Disponible y stock > 0."""
    return Lote.query.filter(
        Lote.estatus == 'Disponible',
        Lote.totalMateria > 0,
    )


def _lotes_para_materia_prima(id_materia_prima):
    """Lotes disponibles para una materia prima especifica
    (los que provienen de compra directa de materia)."""
    return (
        _lotes_disponibles_query()
        .join(MateriaProveida, Lote.idMateriaProveida == MateriaProveida.idMateriaProveida)
        .filter(MateriaProveida.idMateriaPrima == id_materia_prima)
        .order_by(
            Lote.fechaCaducidad.is_(None),
            Lote.fechaCaducidad.asc(),
            Lote.idLote.asc(),
        )
        .all()
    )


def _serializar_lote(lote):
    """Convierte un Lote (compra directa) a dict para mostrar en select."""
    mp = lote.materiaProveida
    unidad = mp.unidadMedida.nombreUnidadMedida if mp and mp.unidadMedida else '—'
    proveedor = mp.proveedor.nombre if mp and mp.proveedor else '—'
    orden = lote.ordenCompra
    return {
        'id':           lote.idLote,
        'lote':         (orden.numeroLote if orden else None) or lote.numeroLote or f'#{lote.idLote}',
        'totalMateria': lote.totalMateria,
        'unidad':       unidad,
        'proveedor':    proveedor,
        'caducidad':    lote.fechaCaducidad.strftime('%d/%m/%Y') if lote.fechaCaducidad else '—',
    }


def _canal_cortes_disponibles_para(id_corte):
    """Canal_corte listos para procesar con un idCorte:
    estatus Disponible y CantidadObtenida is NULL."""
    return (
        CanalCorte.query
        .filter(CanalCorte.idCorte == id_corte)
        .filter(CanalCorte.estatus == 'Disponible')
        .filter(CanalCorte.CantidadObtenida.is_(None))
        .order_by(CanalCorte.idCanalCorte.asc())
        .all()
    )


def _serializar_canal_corte(cc):
    """Convierte un CanalCorte a dict para mostrar en select."""
    canal = Canal.query.get(cc.idCanal)
    cat = canal.categoria if canal else None
    return {
        'id':               cc.idCanalCorte,
        'idCanal':          cc.idCanal,
        'cantidadEsperada': cc.CantidadEsperada,
        'pesoCanal':        canal.Peso if canal else None,
        'categoria':        cat.nombreCategoria if cat else '—',
        'fechaSacrificio':  canal.fechaSacrificio.strftime('%d/%m/%Y') if canal and canal.fechaSacrificio else '—',
    }


def _cortes_con_disponibilidad():
    """Catalogo de cortes (usado como lista de 'recetas de corte'), cada uno
    enriquecido con el numero de canal_corte disponibles para procesar.
    No se devuelven cortes cuyo Porcentaje sea NULL/0 — esos no pueden generar
    canal_cortes."""
    cortes = Corte.query.order_by(Corte.nombreCorte).all()
    items = []
    for c in cortes:
        cat = c.categoria if c else None
        disponibles = (
            CanalCorte.query
            .filter(CanalCorte.idCorte == c.idCorte)
            .filter(CanalCorte.estatus == 'Disponible')
            .filter(CanalCorte.CantidadObtenida.is_(None))
            .count()
        )
        items.append({
            'idCorte':      c.idCorte,
            'nombre':       c.nombreCorte,
            'categoria':    cat.nombreCategoria if cat else '—',
            'porcentaje':   c.Porcentaje,
            'foto_b64':     _foto_b64_de(c.idFoto),
            'disponibles':  disponibles,
        })
    return items


def _generar_numero_lote_produccion():
    """Numero de lote para los Lote producidos por corte.
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
#  LISTADO PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════

@solicitud_de_produccion.route('/solicitudes')
@login_required
@roles_required('admin')
def solicitudes():
    # Lotes disponibles (panel superior, solo los de compra directa)
    lotes_raw = (
        _lotes_disponibles_query()
        .filter(Lote.idMateriaProveida.isnot(None))
        .order_by(
            Lote.fechaCaducidad.is_(None),
            Lote.fechaCaducidad.asc(),
        )
        .all()
    )

    lotes = []
    for l in lotes_raw:
        mp     = l.materiaProveida
        materia = mp.materiaPrima if mp else None
        unidad  = mp.unidadMedida.nombreUnidadMedida if mp and mp.unidadMedida else '—'
        orden   = l.ordenCompra
        lotes.append({
            'id':            l.idLote,
            'lote':          (orden.numeroLote if orden else None) or l.numeroLote or f'#{l.idLote}',
            'materia':       materia.nombreMateriaPrima if materia else '—',
            'totalMateria':  l.totalMateria,
            'unidad':        unidad,
            'caducidad':     l.fechaCaducidad,
        })

    solicitudes_lista = (
        SolicitudProduccion.query
        .order_by(SolicitudProduccion.fechaSolicitud.desc())
        .all()
    )

    return render_template(
        'admin/solicitud_produccion/solicitudes.html',
        lotes=lotes,
        solicitudes=solicitudes_lista,
    )


# ═════════════════════════════════════════════════════════════════════════════
#  NUEVA SOLICITUD — ruteador segun tipoReceta
# ═════════════════════════════════════════════════════════════════════════════

@solicitud_de_produccion.route('/solicitudes/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def solicitudes_nueva():
    """Pagina unificada para crear solicitud de cualquier tipo.
    El query string ?tipo=Personalizada|Corte controla que catalogo se muestra."""

    tipo = request.values.get('tipo', 'Personalizada')
    if tipo not in ('Personalizada', 'Corte'):
        tipo = 'Personalizada'

    if tipo == 'Corte':
        return _solicitud_nueva_corte()
    return _solicitud_nueva_personalizada()


# ─────────────────────────────────────────────────────────────────────────────
#  Tipo Personalizada — consume Lote, produce Producto
# ─────────────────────────────────────────────────────────────────────────────

def _solicitud_nueva_personalizada():
    recetas_lista = Receta.query.order_by(Receta.nombreReceta).all()

    receta_seleccionada = None
    materias_con_lotes  = []
    cantidad_producir   = 1

    receta_id_get = request.args.get('idReceta', type=int)
    if receta_id_get:
        receta_seleccionada = Receta.query.get(receta_id_get)

    if request.method == 'POST':
        try:
            id_receta         = int(request.form.get('idReceta'))
            cantidad_producir = int(request.form.get('cantidadProducir'))
        except (TypeError, ValueError):
            flash('Datos invalidos. Selecciona una receta y una cantidad valida.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Personalizada'))

        if cantidad_producir <= 0:
            flash('La cantidad a producir debe ser mayor a cero.', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Personalizada', idReceta=id_receta,
            ))

        receta_obj = Receta.query.get(id_receta)
        if not receta_obj:
            flash('Receta no encontrada.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Personalizada'))

        ingredientes = receta_obj.materiasPrimas.all()
        seleccion    = []   # [(rmp, lote, cantidadConsumida)]
        errores      = []

        for rmp in ingredientes:
            lote_id = request.form.get(f'lote_{rmp.idMateriaPrima}', type=int)
            if not lote_id:
                errores.append(f'Falta seleccionar lote para "{rmp.materiaPrima.nombreMateriaPrima}".')
                continue

            lote = Lote.query.get(lote_id)
            if not lote or lote.estatus != 'Disponible':
                errores.append(f'El lote elegido para "{rmp.materiaPrima.nombreMateriaPrima}" ya no esta disponible.')
                continue

            if not lote.materiaProveida or lote.materiaProveida.idMateriaPrima != rmp.idMateriaPrima:
                errores.append(f'Lote invalido para "{rmp.materiaPrima.nombreMateriaPrima}".')
                continue

            cantidad_necesaria = rmp.cantidadUsada * cantidad_producir
            if (lote.totalMateria or 0) < cantidad_necesaria:
                errores.append(
                    f'Stock insuficiente en lote {lote.numeroLote or lote.idLote} '
                    f'para "{rmp.materiaPrima.nombreMateriaPrima}". '
                    f'Necesario: {cantidad_necesaria:g}, disponible: {lote.totalMateria:g}.'
                )
                continue

            seleccion.append((rmp, lote, cantidad_necesaria))

        if errores:
            for e in errores:
                flash(e, 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Personalizada', idReceta=id_receta,
            ))

        try:
            nueva = SolicitudProduccion(
                tipoReceta       = 'Personalizada',
                idReceta         = receta_obj.idReceta,
                idCorte          = None,
                cantidadProducir = cantidad_producir,
                fechaSolicitud   = datetime.now(),
                fechaCompletada  = datetime.now(),
                estatus          = 'Completada',
                idUsuario        = current_user.id if current_user and current_user.is_authenticated else None,
                notas            = (request.form.get('notas') or '').strip() or None,
            )
            db.session.add(nueva)
            db.session.flush()

            for rmp, lote, cant in seleccion:
                db.session.add(SolicitudProduccionDetalle(
                    idSolicitud       = nueva.idSolicitud,
                    idMateriaPrima    = rmp.idMateriaPrima,
                    idLote            = lote.idLote,
                    cantidadConsumida = cant,
                ))
                lote.totalMateria = (lote.totalMateria or 0) - cant
                if lote.totalMateria <= 0:
                    lote.totalMateria = 0
                    lote.estatus      = 'Agotado'

            producto = receta_obj.producto
            if producto is not None:
                producto.StockProducto = (producto.StockProducto or 0) + cantidad_producir

            db.session.commit()
            flash(
                f'Solicitud de produccion creada. Se produjeron {cantidad_producir} unidad(es) '
                f'de "{receta_obj.nombreReceta}".',
                'success'
            )
            return redirect(url_for('solicitud_de_produccion.solicitudes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la solicitud: {e}', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Personalizada', idReceta=id_receta,
            ))

    if receta_seleccionada:
        for rmp in receta_seleccionada.materiasPrimas.all():
            lotes = _lotes_para_materia_prima(rmp.idMateriaPrima)
            materias_con_lotes.append({
                'rmp':             rmp,
                'materia':         rmp.materiaPrima,
                'cantidad_unidad': rmp.cantidadUsada,
                'lotes':           [_serializar_lote(l) for l in lotes],
            })

    return render_template(
        'admin/solicitud_produccion/solicitudes_form.html',
        tipo='Personalizada',
        recetas=recetas_lista,
        receta_seleccionada=receta_seleccionada,
        materias_con_lotes=materias_con_lotes,
        cantidad_producir=cantidad_producir,
        # placeholders para compatibilidad con el template unificado
        cortes_catalogo=[],
        corte_seleccionado=None,
        canal_cortes=[],
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Tipo Corte — consume canal_corte, produce Lote
#  El catalogo de "recetas de corte" es la tabla Corte directamente.
# ─────────────────────────────────────────────────────────────────────────────

def _solicitud_nueva_corte():
    cortes_catalogo = _cortes_con_disponibilidad()

    corte_seleccionado       = None
    canal_cortes_disponibles = []

    corte_id_get = request.args.get('idCorte', type=int)
    if corte_id_get:
        corte_seleccionado = Corte.query.get(corte_id_get)

    if request.method == 'POST':
        try:
            id_corte          = int(request.form.get('idCorte'))
            id_canal_corte    = int(request.form.get('idCanalCorte'))
            cantidad_obtenida = float(request.form.get('cantidadObtenida') or 0)
        except (TypeError, ValueError):
            flash('Datos invalidos. Verifica los campos del formulario.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Corte'))

        corte = Corte.query.get(id_corte)
        if not corte:
            flash('Corte no encontrado.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Corte'))

        canal_corte = CanalCorte.query.get(id_canal_corte)
        if not canal_corte:
            flash('Canal corte no encontrado.', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Corte', idCorte=id_corte,
            ))

        if canal_corte.estatus != 'Disponible' or canal_corte.CantidadObtenida is not None:
            flash('Ese canal corte ya fue procesado.', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Corte', idCorte=id_corte,
            ))

        if canal_corte.idCorte != corte.idCorte:
            flash('El canal corte no corresponde al corte seleccionado.', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Corte', idCorte=id_corte,
            ))

        if cantidad_obtenida <= 0:
            flash('La cantidad obtenida debe ser mayor a cero.', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Corte', idCorte=id_corte,
            ))

        try:
            esperada = canal_corte.CantidadEsperada or 0
            merma    = round(esperada - cantidad_obtenida, 3)

            # 1) Marcar el canal_corte como procesado
            canal_corte.CantidadObtenida = cantidad_obtenida
            canal_corte.Merma            = merma
            canal_corte.estatus          = 'Consumido'

            # 2) Crear el Lote producido
            numero_lote = _generar_numero_lote_produccion()
            lote_producido = Lote(
                idCanalCorte      = canal_corte.idCanalCorte,
                idMateriaProveida = None,
                idOrdenCompra     = None,
                numeroLote        = numero_lote,
                cantidadDeUnidad  = 1,
                cantidadPorUnidad = cantidad_obtenida,
                totalMateria      = cantidad_obtenida,
                precioPorUnidad   = 0.0,
                totalCosto        = 0.0,
                fechaCaducidad    = None,
                estatus           = 'Disponible',
            )
            db.session.add(lote_producido)
            db.session.flush()

            # 3) Crear la solicitud de produccion apuntando directo al Corte
            nueva = SolicitudProduccion(
                tipoReceta       = 'Corte',
                idReceta         = None,
                idCorte          = corte.idCorte,
                cantidadProducir = 1,
                fechaSolicitud   = datetime.now(),
                fechaCompletada  = datetime.now(),
                estatus          = 'Completada',
                idUsuario        = current_user.id if current_user and current_user.is_authenticated else None,
                notas            = (request.form.get('notas') or '').strip() or None,
            )
            db.session.add(nueva)
            db.session.flush()

            db.session.add(SolicitudProduccionDetalle(
                idSolicitud       = nueva.idSolicitud,
                idMateriaPrima    = None,
                idLote            = None,
                idCanalCorte      = canal_corte.idCanalCorte,
                idLoteProducido   = lote_producido.idLote,
                cantidadConsumida = cantidad_obtenida,
            ))

            db.session.commit()
            cat_nombre = corte.categoria.nombreCategoria if corte.categoria else ''
            nombre_corte = f'{corte.nombreCorte} ({cat_nombre})' if cat_nombre else corte.nombreCorte
            flash(
                f'Corte "{nombre_corte}" procesado. '
                f'Se genero el lote {numero_lote} con {cantidad_obtenida:g} kg '
                f'(merma: {merma:g} kg).',
                'success'
            )
            return redirect(url_for('solicitud_de_produccion.solicitudes'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar el corte: {e}', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Corte', idCorte=id_corte,
            ))

    if corte_seleccionado:
        cortes_libres = _canal_cortes_disponibles_para(corte_seleccionado.idCorte)
        canal_cortes_disponibles = [_serializar_canal_corte(cc) for cc in cortes_libres]

    return render_template(
        'admin/solicitud_produccion/solicitudes_form.html',
        tipo='Corte',
        cortes_catalogo=cortes_catalogo,
        corte_seleccionado=corte_seleccionado,
        corte_seleccionado_foto=_foto_b64_de(corte_seleccionado.idFoto) if corte_seleccionado else None,
        canal_cortes=canal_cortes_disponibles,
        # placeholders para compatibilidad con el template unificado
        recetas=[],
        receta_seleccionada=None,
        materias_con_lotes=[],
        cantidad_producir=1,
    )


# ═════════════════════════════════════════════════════════════════════════════
#  CANCELAR (solo deja registro)
# ═════════════════════════════════════════════════════════════════════════════

@solicitud_de_produccion.route('/solicitudes/<int:id>/cancelar', methods=['POST'])
@login_required
@roles_required('admin')
def solicitudes_cancelar(id):
    sol = SolicitudProduccion.query.get_or_404(id)
    if sol.estatus == 'Completada':
        flash('No se puede cancelar una solicitud ya completada.', 'warning')
    else:
        sol.estatus = 'Cancelada'
        db.session.commit()
        flash('Solicitud cancelada.', 'success')
    return redirect(url_for('solicitud_de_produccion.solicitudes'))
