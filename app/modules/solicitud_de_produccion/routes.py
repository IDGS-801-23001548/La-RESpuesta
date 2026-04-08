from flask import render_template, redirect, url_for, flash, request, jsonify
from . import solicitud_de_produccion
from app.extensions import db
from app.models import (
    Receta, RecetaMateriaPrima,
    SolicitudProduccion, SolicitudProduccionDetalle,
    MateriaPrima, MateriaProveida, Lote,
    UnidadMedida, Proveedor, Producto,
)
from flask_login import login_required, current_user
from flask_security import roles_required
from datetime import datetime


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _lotes_disponibles_query():
    """Lotes (Lote) Disponible y con totalMateria > 0."""
    return (
        Lote.query
        .filter(Lote.estatus == 'Disponible')
        .filter(Lote.totalMateria > 0)
    )


def _lotes_para_materia_prima(id_materia_prima):
    """Devuelve lotes disponibles para una materia prima especifica
    (atravesando MateriaProveida)."""
    return (
        _lotes_disponibles_query()
        .join(MateriaProveida, Lote.idMateriaProveida == MateriaProveida.idMateriaProveida)
        .filter(MateriaProveida.idMateriaPrima == id_materia_prima)
        .order_by(Lote.fechaCaducidad.is_(None),
                  Lote.fechaCaducidad.asc(),
                  Lote.idLote.asc())
        .all()
    )


def _serializar_lote(lote):
    """Convierte un Lote a dict para mostrar en select."""
    mp = lote.materiaProveida
    unidad = mp.unidadMedida.nombreUnidadMedida if mp and mp.unidadMedida else '—'
    proveedor = mp.proveedor.nombre if mp and mp.proveedor else '—'
    orden = lote.ordenCompra
    return {
        'id':         lote.idLote,
        'lote':       orden.numeroLote if orden else f'#{lote.idLote}',
        'totalMateria': lote.totalMateria,
        'unidad':     unidad,
        'proveedor':  proveedor,
        'caducidad':  lote.fechaCaducidad.strftime('%d/%m/%Y') if lote.fechaCaducidad else '—',
    }


# ─────────────────────────────────────────────
#  LISTADO PRINCIPAL
# ─────────────────────────────────────────────

@solicitud_de_produccion.route('/solicitudes')
@login_required
@roles_required('admin')
def solicitudes():
    # Lotes disponibles (panel superior)
    lotes_raw = (
        _lotes_disponibles_query()
        .order_by(
            Lote.fechaCaducidad.is_(None),
            Lote.fechaCaducidad.asc()
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
            'lote':          orden.numeroLote if orden else f'#{l.idLote}',
            'materia':       materia.nombreMateriaPrima if materia else '—',
            'totalMateria':  l.totalMateria,
            'unidad':        unidad,
            'caducidad':     l.fechaCaducidad,
        })

    # Solicitudes existentes
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


# ─────────────────────────────────────────────
#  NUEVA SOLICITUD
# ─────────────────────────────────────────────

@solicitud_de_produccion.route('/solicitudes/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def solicitudes_nueva():
    recetas_lista = Receta.query.order_by(Receta.nombreReceta).all()

    # Variables que se pasan en GET y en POST con error
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
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva'))

        if cantidad_producir <= 0:
            flash('La cantidad a producir debe ser mayor a cero.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', idReceta=id_receta))

        receta_obj = Receta.query.get(id_receta)
        if not receta_obj:
            flash('Receta no encontrada.', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva'))

        # Recoger lotes elegidos: input lote_<idMateriaPrima>
        ingredientes = receta_obj.materiasPrimas.all()
        seleccion    = []  # [(rmp, lote, cantidadConsumida)]
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

            # Validar que el lote pertenece a la materia prima correcta
            if not lote.materiaProveida or lote.materiaProveida.idMateriaPrima != rmp.idMateriaPrima:
                errores.append(f'Lote invalido para "{rmp.materiaPrima.nombreMateriaPrima}".')
                continue

            cantidad_necesaria = rmp.cantidadUsada * cantidad_producir
            if lote.totalMateria < cantidad_necesaria:
                errores.append(
                    f'Stock insuficiente en lote {lote.ordenCompra.numeroLote if lote.ordenCompra else lote.idLote} '
                    f'para "{rmp.materiaPrima.nombreMateriaPrima}". '
                    f'Necesario: {cantidad_necesaria:g}, disponible: {lote.totalMateria:g}.'
                )
                continue

            seleccion.append((rmp, lote, cantidad_necesaria))

        if errores:
            for e in errores:
                flash(e, 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', idReceta=id_receta))

        # Todo OK → crear solicitud, descontar stock, sumar al producto
        try:
            nueva = SolicitudProduccion(
                idReceta         = receta_obj.idReceta,
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
                    idSolicitud            = nueva.idSolicitud,
                    idMateriaPrima         = rmp.idMateriaPrima,
                    idLote = lote.idLote,
                    cantidadConsumida      = cant,
                ))
                # Descontar del lote
                lote.totalMateria = lote.totalMateria - cant
                if lote.totalMateria <= 0:
                    lote.totalMateria = 0
                    lote.estatus      = 'Agotado'

            # Aumentar stock del producto terminado
            producto = receta_obj.producto
            if producto is not None:
                producto.StockProducto = (producto.StockProducto or 0) + cantidad_producir

            db.session.commit()
            flash(f'Solicitud de produccion creada. Se produjeron {cantidad_producir} unidad(es) de "{receta_obj.nombreReceta}".', 'success')
            return redirect(url_for('solicitud_de_produccion.solicitudes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la solicitud: {e}', 'danger')
            return redirect(url_for('solicitud_de_produccion.solicitudes_nueva', idReceta=id_receta))

    # ── GET: armar info de la receta seleccionada ──
    if receta_seleccionada:
        for rmp in receta_seleccionada.materiasPrimas.all():
            lotes = _lotes_para_materia_prima(rmp.idMateriaPrima)
            materias_con_lotes.append({
                'rmp':            rmp,
                'materia':        rmp.materiaPrima,
                'cantidad_unidad': rmp.cantidadUsada,
                'lotes':          [_serializar_lote(l) for l in lotes],
            })

    return render_template(
        'admin/solicitud_produccion/solicitudes_form.html',
        recetas=recetas_lista,
        receta_seleccionada=receta_seleccionada,
        materias_con_lotes=materias_con_lotes,
        cantidad_producir=cantidad_producir,
    )


# ─────────────────────────────────────────────
#  CANCELAR (solo deja registro)
# ─────────────────────────────────────────────

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
