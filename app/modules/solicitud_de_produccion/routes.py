from flask import render_template, redirect, url_for, flash, request, jsonify
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
                    idMateriaPrima    = rmp.idMateriaPrima,  # None para cortes
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
            flash(
                f'Solicitud de corte "{nombre_corte}" creada como Pendiente. '
                f'Complétala en el modulo de Produccion.',
                'success'
            )
            return redirect(url_for('solicitud_de_produccion.solicitudes'))

        except Exception as e:
            db.session.rollback()
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
        flash('Solicitud cancelada.', 'success')
    return redirect(url_for('solicitud_de_produccion.solicitudes'))
