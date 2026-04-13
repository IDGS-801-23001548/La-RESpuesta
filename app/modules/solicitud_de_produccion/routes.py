from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from . import solicitud_de_produccion
from app.extensions import db, mongo_fotos
from app.models import (
    Receta, RecetaMateriaPrima,
    SolicitudProduccion, SolicitudProduccionDetalle,
    MateriaPrima, MateriaProveida, Lote,
    Producto,
    Canal, CanalCorte, Corte, ProductoUnitario
)
from flask_login import login_required, current_user
from flask_security import roles_required
from datetime import datetime, date


# ═════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _foto_b64_de(id_foto):
    """Devuelve la foto en base64 desde MongoDB."""
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


def _lotes_materia_disponibles():
    """Lotes provenientes de compra directa de materia prima."""
    lotes_raw = (
        _lotes_disponibles_query()
        .filter(Lote.idMateriaProveida.isnot(None))
        .order_by(
            Lote.fechaCaducidad.is_(None),
            Lote.fechaCaducidad.asc(),
        )
        .all()
    )
    items = []
    for l in lotes_raw:
        mp      = l.materiaProveida
        materia = mp.materiaPrima if mp else None
        unidad  = mp.unidadMedida.nombreUnidadMedida if mp and mp.unidadMedida else '—'
        orden   = l.ordenCompra
        items.append({
            'id':           l.idLote,
            'lote':         (orden.numeroLote if orden else None) or l.numeroLote or f'#{l.idLote}',
            'materia':      materia.nombreMateriaPrima if materia else '—',
            'totalMateria': l.totalMateria,
            'unidad':       unidad,
            'caducidad':    l.fechaCaducidad,
        })
    return items


def _lotes_corte_disponibles():
    """Lotes provenientes de produccion (canal_corte procesado)."""
    lotes_raw = (
        _lotes_disponibles_query()
        .filter(Lote.idCanalCorte.isnot(None))
        .order_by(Lote.idLote.desc())
        .all()
    )
    items = []
    for l in lotes_raw:
        cc = CanalCorte.query.get(l.idCanalCorte)
        corte = Corte.query.get(cc.idCorte) if cc else None
        canal = Canal.query.get(cc.idCanal) if cc else None
        cat = corte.categoria if corte else None
        items.append({
            'id':           l.idLote,
            'lote':         l.numeroLote or f'#{l.idLote}',
            'corte':        corte.nombreCorte if corte else '—',
            'categoria':    cat.nombreCategoria if cat else '—',
            'canal_id':     canal.idCanal if canal else '—',
            'totalMateria': l.totalMateria,
            'unidad':       'kg',
        })
    return items


def _lotes_para_materia_prima(id_materia_prima):
    """Lotes disponibles para una materia prima especifica."""
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


def _lotes_para_corte(id_corte):
    """Lotes disponibles para un corte especifico (via canal_corte)."""
    return (
        _lotes_disponibles_query()
        .join(CanalCorte, Lote.idCanalCorte == CanalCorte.idCanalCorte)
        .filter(CanalCorte.idCorte == id_corte)
        .order_by(Lote.idLote.desc())
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


def _serializar_lote_corte(lote):
    """Convierte un Lote (produccion de corte) a dict para mostrar en select."""
    cc = lote.canalCorte
    canal = Canal.query.get(cc.idCanal) if cc else None
    return {
        'id':           lote.idLote,
        'lote':         lote.numeroLote or f'#{lote.idLote}',
        'totalMateria': lote.totalMateria,
        'unidad':       'kg',
        'canal':        f'Canal #{canal.idCanal}' if canal else '—',
        'caducidad':    lote.fechaCaducidad.strftime('%d/%m/%Y') if lote.fechaCaducidad else '—',
    }

def _generar_numero_lote_produccion():
    """Numero de lote para Lote producido por corte."""
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
        except:
            ultimo_num = 0
    else:
        ultimo_num = 0

    return f"{prefijo}{ultimo_num + 1:02d}"


def _generar_numero_lote_producto():
    """Numero de lote para ProductoUnitario."""
    meses_corto = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',
                   7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
    hoy = date.today()
    prefijo = f"PP-{meses_corto[hoy.month]}{hoy.day:02d}"

    ultimo = (
        ProductoUnitario.query
        .filter(ProductoUnitario.NumeroLote.like(f"{prefijo}%"))
        .order_by(ProductoUnitario.NumeroLote.desc())
        .first()
    )

    if ultimo and ultimo.NumeroLote:
        try:
            ultimo_num = int(ultimo.NumeroLote[len(prefijo):])
        except:
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
    lotes_materia = _lotes_materia_disponibles()
    lotes_corte   = _lotes_corte_disponibles()

    solicitudes_lista = (
        SolicitudProduccion.query
        .order_by(SolicitudProduccion.fechaSolicitud.desc())
        .all()
    )

    return render_template(
        'admin/solicitud_produccion/solicitudes.html',
        lotes_materia=lotes_materia,
        lotes_corte=lotes_corte,
        solicitudes=solicitudes_lista,
    )


# ═════════════════════════════════════════════════════════════════════════════
#  NUEVA SOLICITUD — ruteador segun tipoReceta
# ═════════════════════════════════════════════════════════════════════════════

@solicitud_de_produccion.route('/solicitudes/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def solicitudes_nueva():
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
    materias_con_lotes  = []   # ingredientes tipo materia prima
    cortes_con_lotes    = []   # ingredientes tipo corte
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
        seleccion    = []
        errores      = []

        for rmp in ingredientes:
            nombre_ing = rmp.nombre_ingrediente
            cantidad_necesaria = rmp.cantidadUsada * cantidad_producir

            if rmp.idMateriaPrima:
                # ── Ingrediente tipo materia prima ──
                lote_id = request.form.get(f'lote_materia_{rmp.idMateriaPrima}', type=int)
                if not lote_id:
                    errores.append(f'Falta seleccionar lote para "{nombre_ing}".')
                    continue

                lote = Lote.query.get(lote_id)
                if not lote or lote.estatus != 'Disponible':
                    errores.append(f'El lote elegido para "{nombre_ing}" ya no esta disponible.')
                    continue

                if not lote.materiaProveida or lote.materiaProveida.idMateriaPrima != rmp.idMateriaPrima:
                    errores.append(f'Lote invalido para "{nombre_ing}".')
                    continue

            elif rmp.idCorte:
                # ── Ingrediente tipo corte ──
                lote_id = request.form.get(f'lote_corte_{rmp.idCorte}', type=int)
                if not lote_id:
                    errores.append(f'Falta seleccionar lote para "{nombre_ing}".')
                    continue

                lote = Lote.query.get(lote_id)
                if not lote or lote.estatus != 'Disponible':
                    errores.append(f'El lote elegido para "{nombre_ing}" ya no esta disponible.')
                    continue

                # Validar que el lote pertenece al corte correcto (via canal_corte)
                cc = lote.canalCorte
                if not cc or cc.idCorte != rmp.idCorte:
                    errores.append(f'Lote invalido para "{nombre_ing}".')
                    continue
            else:
                continue  # ingrediente sin FK — ignorar

            if (lote.totalMateria or 0) < cantidad_necesaria:
                errores.append(
                    f'Stock insuficiente en lote {lote.numeroLote or lote.idLote} '
                    f'para "{nombre_ing}". '
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
                fechaCompletada  = None,
                estatus          = 'Pendiente',
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
                    idCanalCorte      = None,
                    idLoteProducido   = None,
                    cantidadConsumida = cant,
                ))

            db.session.commit()

            email_usuario = current_user.email if current_user and current_user.is_authenticated else 'sistema'
            current_app.logger.info(
                f"Solicitud de produccion creada (Personalizada) | receta={receta_obj.nombreReceta} "
                f"| cantidad={cantidad_producir} uds | solicitud=#{nueva.idSolicitud} "
                f"| usuario={email_usuario} | ip={request.remote_addr}"
            )

            flash(
                f'Solicitud de produccion creada como Pendiente para '
                f'"{receta_obj.nombreReceta}" ({cantidad_producir} unidades). '
                f'Un administrador debe autorizarla en Produccion.',
                'success'
            )
            return redirect(url_for('solicitud_de_produccion.solicitudes'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f"Error al crear solicitud (Personalizada) | receta={receta_obj.nombreReceta} | error={e}"
            )
            flash(f'Error al crear la solicitud: {e}', 'danger')
            return redirect(url_for(
                'solicitud_de_produccion.solicitudes_nueva',
                tipo='Personalizada', idReceta=id_receta,
            ))

    # ── GET: construir listas de ingredientes con sus lotes disponibles ──
    if receta_seleccionada:
        for rmp in receta_seleccionada.materiasPrimas.all():
            if rmp.idMateriaPrima:
                lotes = _lotes_para_materia_prima(rmp.idMateriaPrima)
                materias_con_lotes.append({
                    'rmp':             rmp,
                    'id_campo':        rmp.idMateriaPrima,
                    'nombre':          rmp.materiaPrima.nombreMateriaPrima if rmp.materiaPrima else '—',
                    'cantidad_unidad': rmp.cantidadUsada,
                    'lotes':           [_serializar_lote(l) for l in lotes],
                })
            elif rmp.idCorte:
                lotes = _lotes_para_corte(rmp.idCorte)
                corte_obj = rmp.corte
                cat = corte_obj.categoria if corte_obj else None
                nombre = f"{corte_obj.nombreCorte} ({cat.nombreCategoria})" if (corte_obj and cat) else (corte_obj.nombreCorte if corte_obj else '—')
                cortes_con_lotes.append({
                    'rmp':             rmp,
                    'id_campo':        rmp.idCorte,
                    'nombre':          nombre,
                    'cantidad_unidad': rmp.cantidadUsada,
                    'lotes':           [_serializar_lote_corte(l) for l in lotes],
                })

    return render_template(
        'admin/solicitud_produccion/solicitudes_form.html',
        tipo='Personalizada',
        recetas=recetas_lista,
        receta_seleccionada=receta_seleccionada,
        materias_con_lotes=materias_con_lotes,
        cortes_con_lotes=cortes_con_lotes,
        cantidad_producir=cantidad_producir,
        # placeholders para compatibilidad con el template unificado
        canales=[],
        canal_cortes=[],
        corte_seleccionado=None,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Tipo Corte — selecciona canal → corte (canal_corte), crea solicitud Pendiente
#  NO pide cantidad obtenida aqui; eso se hace en el modulo de Produccion
# ─────────────────────────────────────────────────────────────────────────────

def _solicitud_nueva_corte():
    # Canales que tienen al menos 1 canal_corte Disponible (sin CantidadObtenida)
    canales_con_cortes = (
        db.session.query(Canal)
        .join(CanalCorte, CanalCorte.idCanal == Canal.idCanal)
        .filter(CanalCorte.estatus == 'Disponible')
        .filter(CanalCorte.CantidadObtenida.is_(None))
        .distinct()
        .order_by(Canal.idCanal.desc())
        .all()
    )
    canales_data = []
    for c in canales_con_cortes:
        cat = c.categoria
        canales_data.append({
            'idCanal':     c.idCanal,
            'categoria':   cat.nombreCategoria if cat else '—',
            'peso':        c.Peso,
            'fecha':       c.fechaSacrificio.strftime('%d/%m/%Y') if c.fechaSacrificio else '—',
            'descripcion': c.Descripcion or '',
        })

    canal_id_get = request.args.get('idCanal', type=int)
    canal_cortes_disponibles = []
    corte_seleccionado = None

    if canal_id_get:
        # Traer canal_cortes disponibles de esa canal
        ccs = (
            CanalCorte.query
            .filter(CanalCorte.idCanal == canal_id_get)
            .filter(CanalCorte.estatus == 'Disponible')
            .filter(CanalCorte.CantidadObtenida.is_(None))
            .order_by(CanalCorte.idCanalCorte.asc())
            .all()
        )
        for cc in ccs:
            corte = Corte.query.get(cc.idCorte)
            canal_cortes_disponibles.append({
                'idCanalCorte':    cc.idCanalCorte,
                'idCorte':         cc.idCorte,
                'nombreCorte':     corte.nombreCorte if corte else '—',
                'cantidadEsperada': cc.CantidadEsperada,
                'foto_b64':        _foto_b64_de(corte.idFoto) if corte else None,
            })

    if request.method == 'POST':
        try:
            id_canal_corte = int(request.form.get('idCanalCorte'))
        except (TypeError, ValueError):
            flash('Debes seleccionar un canal corte.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Corte', idCanal=canal_id_get))

        canal_corte = CanalCorte.query.get(id_canal_corte)
        if not canal_corte:
            flash('Canal corte no encontrado.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Corte'))

        if canal_corte.estatus != 'Disponible' or canal_corte.CantidadObtenida is not None:
            flash('Ese canal corte ya fue procesado.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Corte', idCanal=canal_id_get))

        corte = Corte.query.get(canal_corte.idCorte)

        try:
            # Crear solicitud en estado Pendiente — se completa en modulo Produccion
            nueva = SolicitudProduccion(
                tipoReceta       = 'Corte',
                idReceta         = None,
                idCorte          = corte.idCorte if corte else canal_corte.idCorte,
                cantidadProducir = 1,
                fechaSolicitud   = datetime.now(),
                fechaCompletada  = None,
                estatus          = 'Pendiente',
                idUsuario        = current_user.id if current_user and current_user.is_authenticated else None,
                notas            = (request.form.get('notas') or '').strip() or None,
            )
            db.session.add(nueva)
            db.session.flush()

            # Guardar detalle con el canal_corte elegido (sin lote producido aun)
            db.session.add(SolicitudProduccionDetalle(
                idSolicitud       = nueva.idSolicitud,
                idMateriaPrima    = None,
                idLote            = None,
                idCanalCorte      = canal_corte.idCanalCorte,
                idLoteProducido   = None,
                cantidadConsumida = 0,
            ))

            db.session.commit()
            cat_nombre = corte.categoria.nombreCategoria if (corte and corte.categoria) else ''
            nombre_corte = f'{corte.nombreCorte} ({cat_nombre})' if (corte and cat_nombre) else (corte.nombreCorte if corte else '—')

            email_usuario = current_user.email if current_user and current_user.is_authenticated else 'sistema'
            current_app.logger.info(
                f"Solicitud de produccion creada (Corte) | corte={nombre_corte} "
                f"| canal=#{canal_corte.idCanal} | solicitud=#{nueva.idSolicitud} "
                f"| usuario={email_usuario} | ip={request.remote_addr}"
            )

            flash(
                f'Solicitud de corte "{nombre_corte}" creada como Pendiente. '
                f'Complétala en el modulo de Produccion.',
                'success'
            )
            return redirect(url_for('solicitud_de_produccion.solicitudes'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f"Error al crear solicitud (Corte) | canal_corte=#{id_canal_corte} | error={e}"
            )
            flash(f'Error al crear la solicitud: {e}', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', tipo='Corte', idCanal=canal_id_get))

    return render_template(
        'admin/solicitud_produccion/solicitudes_form.html',
        tipo='Corte',
        canales=canales_data,
        canal_id_seleccionado=canal_id_get,
        canal_cortes=canal_cortes_disponibles,
        corte_seleccionado=corte_seleccionado,
        # placeholders
        recetas=[],
        receta_seleccionada=None,
        materias_con_lotes=[],
        cortes_con_lotes=[],
        cantidad_producir=1,
    )


# ═════════════════════════════════════════════════════════════════════════════
#  API AJAX — canal_cortes por canal
# ═════════════════════════════════════════════════════════════════════════════

@solicitud_de_produccion.route('/solicitudes/api/canal-cortes/<int:canal_id>', methods=['GET'])
@login_required
@roles_required('admin')
def api_canal_cortes_por_canal(canal_id):
    """Devuelve JSON con canal_cortes disponibles para una canal dada."""
    ccs = (
        CanalCorte.query
        .filter(CanalCorte.idCanal == canal_id)
        .filter(CanalCorte.estatus == 'Disponible')
        .filter(CanalCorte.CantidadObtenida.is_(None))
        .order_by(CanalCorte.idCanalCorte.asc())
        .all()
    )
    result = []
    for cc in ccs:
        corte = Corte.query.get(cc.idCorte)
        result.append({
            'idCanalCorte':     cc.idCanalCorte,
            'idCorte':          cc.idCorte,
            'nombreCorte':      corte.nombreCorte if corte else '—',
            'cantidadEsperada': cc.CantidadEsperada,
        })
    return jsonify(result)


# ═════════════════════════════════════════════════════════════════════════════
#  CANCELAR
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

        email_usuario = current_user.email if current_user and current_user.is_authenticated else 'sistema'
        current_app.logger.info(
            f"Solicitud de produccion cancelada | solicitud=#{sol.idSolicitud} "
            f"| tipo={sol.tipoReceta} | nombre={sol.nombreReceta or '—'} "
            f"| usuario={email_usuario} | ip={request.remote_addr}"
        )

        flash('Solicitud cancelada.', 'success')
    return redirect(url_for('solicitud_de_produccion.solicitudes'))

# ═════════════════════════════════════════════════════════════════════════════
#  COMPLETAR PRODUCCION
# ═════════════════════════════════════════════════════════════════════════════

def _completar_corte(sol):
    detalle = sol.detalles.first()
    cc = CanalCorte.query.get(detalle.idCanalCorte) if detalle else None
    corte = Corte.query.get(cc.idCorte) if cc else None
    canal = Canal.query.get(cc.idCanal) if cc else None

    if request.method == 'POST':
        cantidad_obtenida = float(request.form.get('cantidadObtenida') or 0)

        if cantidad_obtenida <= 0:
            flash('Cantidad invalida.', 'danger')
            return redirect(request.url)

        try:
            merma = (cc.CantidadEsperada or 0) - cantidad_obtenida

            cc.CantidadObtenida = cantidad_obtenida
            cc.Merma = merma
            cc.estatus = 'Consumido'

            numero_lote = _generar_numero_lote_produccion()

            lote = Lote(
                idCanalCorte=cc.idCanalCorte,
                numeroLote=numero_lote,
                totalMateria=cantidad_obtenida,
                estatus='Disponible',
                idUsuario=current_user.id
            )

            db.session.add(lote)
            db.session.flush()

            sol.estatus = 'Completada'
            sol.fechaCompletada = datetime.now()

            detalle.idLoteProducido = lote.idLote
            detalle.cantidadConsumida = cantidad_obtenida

            db.session.commit()

            flash(f'Corte completado. Lote {numero_lote}', 'success')
            return redirect(url_for('solicitud_de_produccion.solicitudes'))

        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')

    return render_template('admin/produccion/completar_corte.html', solicitud=sol)

def _completar_personalizada(sol):
    detalles = sol.detalles.all()
    receta = sol.receta
    producto = receta.producto if receta else None

    ingredientes_info = []
    for det in detalles:
        lote = Lote.query.get(det.idLote) if det.idLote else None
        mp = det.materiaPrima

        ingredientes_info.append({
            'nombre': mp.nombreMateriaPrima if mp else '—',
            'lote': (lote.numeroLote or f'#{lote.idLote}') if lote else '—',
            'necesario': det.cantidadConsumida,
            'disponible': lote.totalMateria if lote else 0,
            'lote_ok': lote and lote.estatus == 'Disponible' and (lote.totalMateria or 0) >= det.cantidadConsumida,
        })

    info = {
        'nombre': sol.nombreReceta,
        'cantidad_producir': sol.cantidadProducir,
        'foto_b64': _foto_b64_de(receta.idFoto) if receta else None,
        'ingredientes': ingredientes_info,
        'producto': producto.NombreProducto if producto else '—',
    }

    if request.method == 'POST':
        try:
            for det in detalles:
                lote = Lote.query.get(det.idLote)

                if lote.totalMateria < det.cantidadConsumida:
                    raise ValueError('Stock insuficiente')

                lote.totalMateria -= det.cantidadConsumida

                if lote.totalMateria <= 0:
                    lote.estatus = 'Agotado'

            numero_lote = _generar_numero_lote_producto()

            for _ in range(sol.cantidadProducir):
                db.session.add(ProductoUnitario(
                    idProducto=producto.idProducto,
                    NumeroLote=numero_lote,
                    estatus='Disponible'
                ))

            sol.estatus = 'Completada'
            sol.fechaCompletada = datetime.now()

            db.session.commit()

            flash('Producción completada.', 'success')
            return redirect(url_for('solicitud_de_produccion.solicitudes'))

        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')

    return render_template(
        'admin/produccion/produccion_completar.html',
        solicitud=sol,
        info=info,
        tipo='Personalizada'
    )

@solicitud_de_produccion.route('/produccion/<int:id>/completar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def completar_produccion(id):
    sol = SolicitudProduccion.query.get_or_404(id)

    if sol.estatus != 'Pendiente':
        flash('Esta solicitud ya fue completada o cancelada.', 'warning')
        return redirect(url_for('solicitud_de_produccion.solicitudes'))

    if sol.tipoReceta == 'Personalizada':
        return _completar_personalizada(sol)
    return _completar_corte(sol)