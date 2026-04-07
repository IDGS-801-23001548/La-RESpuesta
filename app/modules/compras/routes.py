from collections import defaultdict
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from . import compras
from .forms import OrdenCompraForm
from app.extensions import db
from app.models import (
    Proveedor, MateriaPrima, MateriaProveida,
    MateriaPrimaUnitaria, OrdenCompra,
    ProductoUnitario, Producto, Canal
)
from flask_security import login_required
from flask_security.decorators import roles_required
from datetime import date
from sqlalchemy import func

# ── Mapa de meses en español ──────────────────────────────────────────────────
MESES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}


def _generar_lote():
    """
    Genera número de lote único: MesNombreDDNN  (ej: Abril0501).
    """
    hoy    = date.today()
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


def _parse_date(s):
    """Convierte cadena ISO a date; retorna None si inválida o vacía."""
    try:
        return date.fromisoformat(s) if s else None
    except ValueError:
        return None


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

    # ── Conteo de artículos por orden (3 queries en batch) ───────────────────
    # Tipo Materia: suma de cantidadDeUnidad (ej: 15 cajas)
    mpu_sums = dict(
        db.session.query(
            MateriaPrimaUnitaria.idOrdenCompra,
            func.sum(MateriaPrimaUnitaria.cantidadDeUnidad)
        ).group_by(MateriaPrimaUnitaria.idOrdenCompra).all()
    )

    lotes = [o.numeroLote for o in ordenes if o.numeroLote]

    # Tipo Canal: conteo de canales por lote (cada registro = 1 canal)
    canal_counts = {}
    if lotes:
        canal_counts = dict(
            db.session.query(Canal.numeroLote, func.count(Canal.idCanal))
            .filter(Canal.numeroLote.in_(lotes))
            .group_by(Canal.numeroLote)
            .all()
        )

    # Tipo Producto: conteo de productos distintos por lote
    pu_counts = {}
    if lotes:
        pu_counts = dict(
            db.session.query(
                ProductoUnitario.NumeroLote,
                func.count(func.distinct(ProductoUnitario.idProducto))
            )
            .filter(ProductoUnitario.NumeroLote.in_(lotes))
            .group_by(ProductoUnitario.NumeroLote)
            .all()
        )

    articulos_count = {}
    for o in ordenes:
        total = int(mpu_sums.get(o.idOrdenCompra, 0) or 0)
        total += canal_counts.get(o.numeroLote, 0)
        total += pu_counts.get(o.numeroLote, 0)
        articulos_count[o.idOrdenCompra] = total

    total_en_curso  = sum(1 for o in ordenes if o.estatus == 'EnCurso')
    total_recibida  = sum(1 for o in ordenes if o.estatus == 'Recibida')
    total_cancelada = sum(1 for o in ordenes if o.estatus == 'Cancelada')
    return render_template(
        "admin/compras/compras.html",
        ordenes=ordenes,
        total_en_curso=total_en_curso,
        total_recibida=total_recibida,
        total_cancelada=total_cancelada,
        articulos_count=articulos_count,
    )


# ── Detalle de orden ──────────────────────────────────────────────────────────
@compras.route("/compras/<int:id>", methods=['GET'])
@login_required
@roles_required('admin')
def compra_detalle(id):
    orden = OrdenCompra.query.get_or_404(id)

    # Ítems Materia (MateriaPrimaUnitaria)
    items_materia = orden.materiasPrimasUnitarias.all()

    # Ítems Producto agrupados por idProducto
    pu_lista = ProductoUnitario.query.filter_by(NumeroLote=orden.numeroLote).all()
    pu_por_producto = defaultdict(list)
    for pu in pu_lista:
        pu_por_producto[pu.idProducto].append(pu)
    items_producto = []
    for id_prod, unidades in pu_por_producto.items():
        p = Producto.query.get(id_prod)
        items_producto.append({
            'producto':        p,
            'total':           len(unidades),
            'disponibles':     sum(1 for u in unidades if u.estatus == 'Disponible'),
            'en_espera':       sum(1 for u in unidades if u.estatus == 'EnEspera'),
            'desechados':      sum(1 for u in unidades if u.estatus == 'Desechado'),
            'fecha_caducidad': unidades[0].FechaCaducidad,
        })

    # Ítems Canal agrupados por idMateriaProveida
    canal_lista = Canal.query.filter_by(numeroLote=orden.numeroLote).all()
    canal_por_mp = defaultdict(list)
    for c in canal_lista:
        canal_por_mp[c.idMateriaProveida].append(c)
    items_canal = []
    for id_mp, canales in canal_por_mp.items():
        mp = MateriaProveida.query.get(id_mp)
        items_canal.append({
            'materia_proveida': mp,
            'total':            len(canales),
            'peso_total':       round(sum(c.peso or 0 for c in canales), 3),
            'disponibles':      sum(1 for c in canales if c.estatus == 'Disponible'),
            'en_espera':        sum(1 for c in canales if c.estatus == 'EnEspera'),
            'fecha_sacrificio': canales[0].fechaSacrificio,
        })

    form = OrdenCompraForm()
    return render_template(
        "admin/compras/compras_detalle.html",
        orden=orden,
        items=items_materia,
        items_producto=items_producto,
        items_canal=items_canal,
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
            errores = '; '.join(
                e for field in form for e in field.errors
            ) or 'Token de seguridad inválido.'
            flash(errores, 'danger')
            return redirect(url_for('compras.compra_nueva'))

        proveedor_id = form.proveedor_id.data
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

        # Arrays de líneas
        mp_ids            = request.form.getlist('materia_proveida_id[]')
        cantidades_u      = request.form.getlist('cantidad_de_unidad[]')
        cantidades_x      = request.form.getlist('cantidad_por_unidad[]')
        precios           = request.form.getlist('precio_por_unidad[]')
        fechas_caducidad  = request.form.getlist('fecha_caducidad[]')
        fechas_sacrificio = request.form.getlist('fecha_sacrificio[]')
        pesos_canal       = request.form.getlist('peso_canal[]')

        if not mp_ids:
            flash('Debes agregar al menos una materia prima.', 'danger')
            return redirect(url_for('compras.compra_nueva'))

        total_orden = 0.0
        lineas = []
        errores_linea = []

        for i, mp_id in enumerate(mp_ids):
            num = i + 1
            mp_id  = int(mp_id) if mp_id else 0
            cant_u_raw = cantidades_u[i] if i < len(cantidades_u) else ''
            cant_x_raw = cantidades_x[i] if i < len(cantidades_x) else ''
            precio_raw = precios[i]       if i < len(precios)      else ''

            if not mp_id:
                errores_linea.append(f'Línea {num}: selecciona una materia proveída.')
                continue

            if not cant_u_raw or cant_u_raw.strip() == '':
                errores_linea.append(f'Línea {num}: la cantidad de unidades es obligatoria.')
                continue
            if not precio_raw or precio_raw.strip() == '':
                errores_linea.append(f'Línea {num}: el precio por unidad es obligatorio.')
                continue

            cant_u = float(cant_u_raw)
            cant_x = float(cant_x_raw) if cant_x_raw.strip() else 0.0
            precio = float(precio_raw)

            if cant_u <= 0:
                errores_linea.append(f'Línea {num}: la cantidad debe ser mayor a 0.')
                continue
            if precio <= 0:
                errores_linea.append(f'Línea {num}: el precio debe ser mayor a 0.')
                continue

            # Validar campos condicionales según tipo de materia
            mp_proveida_check = MateriaProveida.query.get(mp_id)
            if mp_proveida_check:
                tipo_check = mp_proveida_check.materiaPrima.tipo or 'Materia'
                if tipo_check == 'Producto':
                    if cant_x <= 0:
                        errores_linea.append(f'Línea {num}: la cantidad por unidad es obligatoria para tipo Producto.')
                        continue
                    fec = fechas_caducidad[i] if i < len(fechas_caducidad) else ''
                    if not fec:
                        errores_linea.append(f'Línea {num}: la fecha de caducidad es obligatoria para tipo Producto.')
                        continue
                elif tipo_check == 'Canal':
                    fec = fechas_sacrificio[i] if i < len(fechas_sacrificio) else ''
                    if not fec:
                        errores_linea.append(f'Línea {num}: la fecha de sacrificio es obligatoria para tipo Canal.')
                        continue

            fecha_cad = _parse_date(fechas_caducidad[i]  if i < len(fechas_caducidad)  else '')
            fecha_sac = _parse_date(fechas_sacrificio[i] if i < len(fechas_sacrificio) else '')
            peso_c    = float(pesos_canal[i]) if i < len(pesos_canal) and pesos_canal[i] else 0.0

            total_costo   = cant_u * precio
            total_materia = cant_u * cant_x
            total_orden  += total_costo
            lineas.append((mp_id, cant_u, cant_x, precio, total_costo, total_materia,
                           fecha_cad, fecha_sac, peso_c))

        if errores_linea:
            for err in errores_linea:
                flash(err, 'danger')
            return redirect(url_for('compras.compra_nueva'))

        if not lineas:
            flash('No se pudo procesar ninguna línea. Revisa los datos ingresados.', 'danger')
            return redirect(url_for('compras.compra_nueva'))

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
        db.session.flush()

        estatus_item = 'Disponible' if estatus == 'Recibida' else 'EnEspera'

        for mp_id, cant_u, cant_x, precio, total_costo, total_materia, fecha_cad, fecha_sac, peso_c in lineas:
            mp_proveida = MateriaProveida.query.get(mp_id)
            if not mp_proveida:
                continue
            materia = mp_proveida.materiaPrima
            tipo    = materia.tipo or 'Materia'

            # ── Tipo Producto → inserts en producto_unitario ─────────────────
            if tipo == 'Producto':
                if not materia.idProducto:
                    flash(
                        f'La materia prima "{materia.nombreMateriaPrima}" es tipo Producto '
                        'pero no tiene un producto vinculado. Se omitió.',
                        'warning'
                    )
                    continue
                n_piezas = max(1, int(round(cant_u * cant_x)))
                for _ in range(n_piezas):
                    pu = ProductoUnitario(
                        idProducto     = materia.idProducto,
                        NumeroLote     = numero_lote,
                        FechaCaducidad = fecha_cad,
                        estatus        = 'Disponible' if estatus == 'Recibida' else 'EnEspera',
                    )
                    db.session.add(pu)

            # ── Tipo Canal → inserts en canal ────────────────────────────────
            elif tipo == 'Canal':
                n_canales = max(1, int(round(cant_u)))
                for _ in range(n_canales):
                    canal = Canal(
                        idMateriaProveida = mp_id,
                        idCategoria       = materia.idCategoria,
                        numeroLote        = numero_lote,
                        peso              = peso_c if peso_c else None,
                        fechaSacrificio   = fecha_sac,
                        estatus           = 'Disponible' if estatus == 'Recibida' else 'EnEspera',
                    )
                    db.session.add(canal)

            # ── Tipo Materia → insert en materia_prima_unitaria ──────────────
            else:
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

        # Materias primas unitarias
        for item in orden.materiasPrimasUnitarias.all():
            if item.estatus == 'EnEspera':
                item.estatus = 'Disponible'

        # Productos unitarios (lote de la orden)
        for pu in ProductoUnitario.query.filter_by(
            NumeroLote=orden.numeroLote, estatus='EnEspera'
        ).all():
            pu.estatus = 'Disponible'

        # Canales (lote de la orden)
        for canal in Canal.query.filter_by(
            numeroLote=orden.numeroLote, estatus='EnEspera'
        ).all():
            canal.estatus = 'Disponible'

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

        # Materias primas unitarias
        for item in orden.materiasPrimasUnitarias.all():
            if item.estatus == 'EnEspera':
                item.estatus = 'Cancelado'

        # Productos unitarios en espera → Desechado
        for pu in ProductoUnitario.query.filter_by(
            NumeroLote=orden.numeroLote, estatus='EnEspera'
        ).all():
            pu.estatus = 'Desechado'

        # Canales en espera → Cancelado
        for canal in Canal.query.filter_by(
            numeroLote=orden.numeroLote, estatus='EnEspera'
        ).all():
            canal.estatus = 'Cancelado'

        db.session.commit()
        flash('Orden cancelada. Los ítems pendientes han sido marcados como cancelados/desechados.', 'warning')
    return redirect(url_for('compras.compra_detalle', id=id))


# ── Vista de impresión ────────────────────────────────────────────────────────
@compras.route("/compras/<int:id>/imprimir", methods=['GET'])
@login_required
@roles_required('admin')
def compra_imprimir(id):
    orden = OrdenCompra.query.get_or_404(id)
    items = orden.materiasPrimasUnitarias.all()

    # Para impresión también mostramos resumen de producto y canal
    pu_lista = ProductoUnitario.query.filter_by(NumeroLote=orden.numeroLote).all()
    pu_por_producto = defaultdict(list)
    for pu in pu_lista:
        pu_por_producto[pu.idProducto].append(pu)
    items_producto = [
        {
            'producto':        Producto.query.get(id_prod),
            'total':           len(unidades),
            'fecha_caducidad': unidades[0].FechaCaducidad,
        }
        for id_prod, unidades in pu_por_producto.items()
    ]

    canal_lista = Canal.query.filter_by(numeroLote=orden.numeroLote).all()
    canal_por_mp = defaultdict(list)
    for c in canal_lista:
        canal_por_mp[c.idMateriaProveida].append(c)
    items_canal = [
        {
            'materia_proveida': MateriaProveida.query.get(id_mp),
            'total':            len(canales),
            'peso_total':       round(sum(c.peso or 0 for c in canales), 3),
            'fecha_sacrificio': canales[0].fechaSacrificio,
        }
        for id_mp, canales in canal_por_mp.items()
    ]

    return render_template(
        "admin/compras/compras_imprimir.html",
        orden=orden,
        items=items,
        items_producto=items_producto,
        items_canal=items_canal,
        today=date.today(),
    )


# ══════════════════════════════════════════════════════════════════════════════
# AJAX — endpoints para selects en cascada
# ══════════════════════════════════════════════════════════════════════════════

@compras.route("/compras/api/materias-primas/<int:proveedor_id>", methods=['GET'])
@login_required
@roles_required('admin')
def api_materias_por_proveedor(proveedor_id):
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
    Devuelve unidad, conversor y ── nuevo ── tipo de la materia prima.
    El campo tipo es usado por el frontend para mostrar campos condicionales
    (fecha_caducidad para Producto, fecha_sacrificio + peso para Canal).
    """
    mp        = MateriaProveida.query.get_or_404(materia_proveida_id)
    unidad    = mp.unidadMedida
    conversor = unidad.conversor if unidad else None
    materia   = mp.materiaPrima

    return jsonify({
        'unidad_medida': unidad.nombreUnidadMedida  if unidad    else '—',
        'conversor':     conversor.nombreConversor   if conversor else '—',
        'tipo':          materia.tipo                if materia   else 'Materia',
    })
