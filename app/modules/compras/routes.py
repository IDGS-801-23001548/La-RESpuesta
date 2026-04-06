from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from . import compras
from .forms import OrdenCompraForm
from app.extensions import db
from app.models import Proveedor, MateriaPrima, MateriaProveida, MateriaPrimaUnitaria, OrdenCompra
from flask_security import login_required
from flask_security.decorators import roles_required
from datetime import date

# ── Mapa de meses en español ──────────────────────────────────────────────────
MESES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}


def _generar_lote():
    """
    Genera número de lote único: MesNombreDDNN  (ej: Abril0501).
    Busca el último lote registrado con el prefijo de hoy (MesDia)
    y toma el sufijo numérico más alto para incrementarlo.
    Esto garantiza unicidad independientemente de la fechaDeOrden
    que el usuario haya elegido en el formulario.
    """
    hoy = date.today()
    mes    = MESES[hoy.month]
    dia    = f"{hoy.day:02d}"
    prefijo = f"{mes}{dia}"

    ultimo = (
        OrdenCompra.query
        .filter(OrdenCompra.numeroLote.like(f"{prefijo}%"))
        .order_by(OrdenCompra.numeroLote.desc())
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


# ── Lista de órdenes ──────────────────────────────────────────────────────────
@compras.route("/compras", methods=['GET'])
@login_required
@roles_required('admin')
def compra():
    ordenes = (
        OrdenCompra.query
        .order_by(OrdenCompra.fechaDeOrden.desc(), OrdenCompra.idOrdenCompra.desc())
        .all()
    )
    total_en_curso  = sum(1 for o in ordenes if o.estatus == 'EnCurso')
    total_recibida  = sum(1 for o in ordenes if o.estatus == 'Recibida')
    total_cancelada = sum(1 for o in ordenes if o.estatus == 'Cancelada')
    return render_template(
        "admin/compras/compras.html",
        ordenes=ordenes,
        total_en_curso=total_en_curso,
        total_recibida=total_recibida,
        total_cancelada=total_cancelada,
    )


# ── Detalle de orden ──────────────────────────────────────────────────────────
@compras.route("/compras/<int:id>", methods=['GET'])
@login_required
@roles_required('admin')
def compra_detalle(id):
    orden = OrdenCompra.query.get_or_404(id)
    items = orden.materiasPrimasUnitarias.all()
    form  = OrdenCompraForm()
    return render_template(
        "admin/compras/compras_detalle.html",
        orden=orden,
        items=items,
        form=form,
        today=date.today(),
    )


# ── Nueva orden ───────────────────────────────────────────────────────────────
@compras.route("/compras/nueva", methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def compra_nueva():
    form = OrdenCompraForm()
    proveedores = Proveedor.query.filter_by(estatus='activo').order_by(Proveedor.nombre).all()

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Token de seguridad inválido. Intenta de nuevo.', 'danger')
            return redirect(url_for('compras.compra_nueva'))

        proveedor_id = request.form.get('proveedor_id', type=int)
        fecha_str    = request.form.get('fecha', '')
        notas        = request.form.get('notas', '').strip()
        estatus      = request.form.get('estatus', 'EnCurso')

        if estatus not in ('EnCurso', 'Recibida'):
            estatus = 'EnCurso'

        proveedor = Proveedor.query.get(proveedor_id)
        if not proveedor or not proveedor.es_activo:
            flash('Proveedor inválido o inactivo.', 'danger')
            return redirect(url_for('compras.compra_nueva'))

        try:
            fecha_orden = date.fromisoformat(fecha_str) if fecha_str else date.today()
        except ValueError:
            fecha_orden = date.today()

        # Leer arrays de líneas
        mp_ids        = request.form.getlist('materia_proveida_id[]')
        cantidades_u  = request.form.getlist('cantidad_de_unidad[]')
        cantidades_x  = request.form.getlist('cantidad_por_unidad[]')
        precios       = request.form.getlist('precio_por_unidad[]')

        if not mp_ids:
            flash('Debes agregar al menos una materia prima.', 'danger')
            return redirect(url_for('compras.compra_nueva'))

        total_orden = 0.0
        lineas = []
        for i, mp_id in enumerate(mp_ids):
            mp_id = int(mp_id) if mp_id else 0
            cant_u = float(cantidades_u[i]) if i < len(cantidades_u) and cantidades_u[i] else 0
            cant_x = float(cantidades_x[i]) if i < len(cantidades_x) and cantidades_x[i] else 0
            precio = float(precios[i])      if i < len(precios)      and precios[i]      else 0
            total_costo   = cant_u * precio
            total_materia = cant_u * cant_x
            total_orden  += total_costo
            lineas.append((mp_id, cant_u, cant_x, precio, total_costo, total_materia))

        numero_lote = _generar_lote()

        orden = OrdenCompra(
            idProveedor  = proveedor_id,
            numeroLote   = numero_lote,
            estatus      = estatus,
            fechaDeOrden = fecha_orden,
            notas        = notas if notas else None,
            totalOrden   = round(total_orden, 2),
        )
        db.session.add(orden)
        db.session.flush()  # obtener idOrdenCompra antes del commit

        # El estatus de los ítems depende del estatus inicial de la orden
        estatus_item = 'Disponible' if estatus == 'Recibida' else 'EnEspera'

        for mp_id, cant_u, cant_x, precio, total_costo, total_materia in lineas:
            item = MateriaPrimaUnitaria(
                idMateriaProveida = mp_id,
                idOrdenCompra     = orden.idOrdenCompra,
                cantidadDeUnidad  = cant_u,
                cantidadPorUnidad = cant_x,
                precioPorUnidad   = precio,
                totalCosto        = round(total_costo, 2),
                totalMateria      = round(total_materia, 4),
                estatus           = estatus_item,
            )
            db.session.add(item)

        db.session.commit()
        flash(f'Orden {numero_lote} registrada correctamente.', 'success')
        return redirect(url_for('compras.compra_detalle', id=orden.idOrdenCompra))

    return render_template(
        "admin/compras/compras_nueva.html",
        form=form,
        proveedores=proveedores,
    )


# ── Cambiar estatus a Recibida ────────────────────────────────────────────────
@compras.route("/compras/<int:id>/recibir", methods=['POST'])
@login_required
@roles_required('admin')
def compra_recibir(id):
    form = OrdenCompraForm()
    if not form.validate_on_submit():
        abort(400)
    orden = OrdenCompra.query.get_or_404(id)
    if orden.estatus == 'EnCurso':
        orden.estatus = 'Recibida'
        # Todos los ítems en espera pasan a Disponible
        for item in orden.materiasPrimasUnitarias.all():
            if item.estatus == 'EnEspera':
                item.estatus = 'Disponible'
        db.session.commit()
        flash('Orden marcada como Recibida. Los ítems ahora están Disponibles.', 'success')
    return redirect(url_for('compras.compra_detalle', id=id))


# ── Cancelar orden ────────────────────────────────────────────────────────────
@compras.route("/compras/<int:id>/cancelar", methods=['POST'])
@login_required
@roles_required('admin')
def compra_cancelar(id):
    form = OrdenCompraForm()
    if not form.validate_on_submit():
        abort(400)
    orden = OrdenCompra.query.get_or_404(id)
    if orden.estatus == 'EnCurso':
        orden.estatus = 'Cancelada'
        # Todos los ítems en espera pasan a Cancelado
        for item in orden.materiasPrimasUnitarias.all():
            if item.estatus == 'EnEspera':
                item.estatus = 'Cancelado'
        db.session.commit()
        flash('Orden cancelada.', 'warning')
    return redirect(url_for('compras.compra_detalle', id=id))


# ── Vista de impresión ────────────────────────────────────────────────────────
@compras.route("/compras/<int:id>/imprimir", methods=['GET'])
@login_required
@roles_required('admin')
def compra_imprimir(id):
    orden = OrdenCompra.query.get_or_404(id)
    items = orden.materiasPrimasUnitarias.all()
    return render_template(
        "admin/compras/compras_imprimir.html",
        orden=orden,
        items=items,
        today=date.today(),
    )


# ══════════════════════════════════════════════════════════════════════════════
# AJAX — endpoints para selects en cascada
# ══════════════════════════════════════════════════════════════════════════════

@compras.route("/compras/api/materias-primas/<int:proveedor_id>", methods=['GET'])
@login_required
@roles_required('admin')
def api_materias_por_proveedor(proveedor_id):
    """
    Devuelve las materias primas disponibles para el proveedor dado
    (las que tienen al menos una MateriaProveida vinculada a ese proveedor).
    """
    registros = (
        db.session.query(MateriaPrima)
        .join(MateriaProveida, MateriaProveida.idMateriaPrima == MateriaPrima.idMateriaPrima)
        .filter(MateriaProveida.idProveedor == proveedor_id)
        .distinct()
        .order_by(MateriaPrima.nombreMateriaPrima)
        .all()
    )
    return jsonify([
        {'id': mp.idMateriaPrima, 'nombre': mp.nombreMateriaPrima}
        for mp in registros
    ])


@compras.route(
    "/compras/api/materias-proveidas/<int:proveedor_id>/<int:materia_prima_id>",
    methods=['GET']
)
@login_required
@roles_required('admin')
def api_materias_proveidas(proveedor_id, materia_prima_id):
    """
    Devuelve las materias proveidas que coinciden con proveedor + materia prima.
    """
    registros = (
        MateriaProveida.query
        .filter_by(idProveedor=proveedor_id, idMateriaPrima=materia_prima_id)
        .order_by(MateriaProveida.nombreMateriaProveida)
        .all()
    )
    return jsonify([
        {'id': mp.idMateriaProveida, 'nombre': mp.nombreMateriaProveida}
        for mp in registros
    ])


@compras.route("/compras/api/detalle-mp/<int:materia_proveida_id>", methods=['GET'])
@login_required
@roles_required('admin')
def api_detalle_mp(materia_proveida_id):
    """
    Devuelve la unidad de medida y el conversor de una materia proveida.
    """
    mp = MateriaProveida.query.get_or_404(materia_proveida_id)
    unidad    = mp.unidadMedida
    conversor = unidad.conversor if unidad else None
    return jsonify({
        'unidad_medida': unidad.nombreUnidadMedida if unidad else '—',
        'conversor':     conversor.nombreConversor  if conversor else '—',
    })
