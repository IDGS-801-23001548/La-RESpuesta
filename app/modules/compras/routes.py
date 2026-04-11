from collections import defaultdict
from types import SimpleNamespace
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from . import compras
from .forms import OrdenCompraForm
from app.extensions import db
from app.models import (
    Proveedor, MateriaPrima, MateriaProveida,
    OrdenCompra, Canal, CanalCorte, Corte, Categoria,
    Lote, ProductoUnitario, Producto,
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


def _parse_float(s):
    """Convierte string a float tolerando comas como separador decimal."""
    if not s:
        return 0.0
    try:
        return float(str(s).replace(',', '.'))
    except ValueError:
        return 0.0


def _parse_int(s):
    """Convierte string a int truncando cualquier parte decimal."""
    if not s:
        return 0
    try:
        return int(float(str(s).replace(',', '.')))
    except ValueError:
        return 0


def _fake_mp_por_categoria(categoria):
    """
    Construye un objeto compatible con los templates (que esperan
    materia_proveida.nombreMateriaProveida y materia_proveida.materiaPrima.nombreMateriaPrima)
    a partir de una Categoria — Canal ya no tiene idMateriaProveida.
    """
    nombre_cat = categoria.nombreCategoria if categoria else '—'
    return SimpleNamespace(
        nombreMateriaProveida=f'Canal — {nombre_cat}',
        materiaPrima=SimpleNamespace(nombreMateriaPrima=nombre_cat),
    )


def _crear_canal_cortes_para(canal):
    """
    Genera automaticamente un registro en canal_corte por cada Corte
    cuya categoria coincide con la categoria de la canal.

    Nota sobre unidades:
    - Corte.Porcentaje esta almacenado como fraccion decimal (ej: 0.065 = 6.5%),
      no como porcentaje entero. Por lo tanto la formula es Peso * Porcentaje,
      no Peso * Porcentaje / 100.
    - El resultado queda expresado en kilogramos (mismas unidades que canal.Peso).
    - La suma de todos los CantidadEsperada para una canal debe dar canal.Peso.

    CantidadEsperada = canal.Peso * Corte.Porcentaje
    CantidadObtenida = NULL  (se llena cuando el corte se procesa en produccion)
    Merma            = NULL
    estatus          = 'Disponible'
    """
    if canal.idCategoria is None or canal.Peso is None:
        return 0

    cortes = Corte.query.filter_by(idCategoria=canal.idCategoria).all()
    creados = 0
    peso = float(canal.Peso)
    for c in cortes:
        porcentaje = float(c.Porcentaje or 0)
        cantidad_esperada = round(peso * porcentaje, 3) if porcentaje else None
        db.session.add(CanalCorte(
            idCorte          = c.idCorte,
            idCanal          = canal.idCanal,
            CantidadEsperada = cantidad_esperada,
            CantidadObtenida = None,
            Merma            = None,
            estatus          = 'Disponible',
        ))
        creados += 1
    return creados


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

    order_ids = [o.idOrdenCompra for o in ordenes]

    # Materia Prima: conteo de lotes (Lote ligado directamente a la orden)
    mp_counts = {}
    if order_ids:
        mp_counts = {
            oc_id: cnt
            for oc_id, cnt in db.session.query(
                Lote.idOrdenCompra,
                func.count(Lote.idLote)
            ).filter(Lote.idOrdenCompra.in_(order_ids))
            .group_by(Lote.idOrdenCompra).all()
        }

    # Canal: conteo por idOrdenCompra
    canal_counts = {}
    if order_ids:
        canal_counts = {
            oc_id: cnt
            for oc_id, cnt in db.session.query(
                Canal.idOrdenCompra,
                func.count(Canal.idCanal)
            ).filter(Canal.idOrdenCompra.in_(order_ids))
            .group_by(Canal.idOrdenCompra).all()
        }

    # Producto Unitario: conteo por idOrdenCompra
    pu_counts = {}
    if order_ids:
        pu_counts = {
            oc_id: cnt
            for oc_id, cnt in db.session.query(
                ProductoUnitario.idOrdenCompra,
                func.count(ProductoUnitario.idProductoUnitario)
            ).filter(ProductoUnitario.idOrdenCompra.in_(order_ids))
            .group_by(ProductoUnitario.idOrdenCompra).all()
        }

    articulos_por_orden = {
        o.idOrdenCompra: (
            mp_counts.get(o.idOrdenCompra, 0) +
            canal_counts.get(o.idOrdenCompra, 0) +
            pu_counts.get(o.idOrdenCompra, 0)
        )
        for o in ordenes
    }

    return render_template(
        "admin/compras/compras.html",
        ordenes=ordenes,
        total_en_curso=total_en_curso,
        total_recibida=total_recibida,
        total_cancelada=total_cancelada,
        articulos_por_orden=articulos_por_orden,
    )


# ── Detalle de orden ──────────────────────────────────────────────────────────
@compras.route("/compras/<int:id>", methods=['GET'])
@login_required
@roles_required('admin')
def compra_detalle(id):
    orden = OrdenCompra.query.get_or_404(id)

    # Ítems Materia (Lote ligado a la orden)
    items_materia = Lote.query.filter_by(idOrdenCompra=orden.idOrdenCompra).all()

    # Ítems Producto agrupados por idProducto
    pu_lista = ProductoUnitario.query.filter_by(idOrdenCompra=orden.idOrdenCompra).all()
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

    # Ítems Canal agrupados por idCategoria
    canal_lista = Canal.query.filter_by(idOrdenCompra=orden.idOrdenCompra).all()
    canal_por_cat = defaultdict(list)
    for c in canal_lista:
        canal_por_cat[c.idCategoria].append(c)
    items_canal = []
    for id_cat, canales in canal_por_cat.items():
        cat = Categoria.query.get(id_cat)
        items_canal.append({
            'materia_proveida': _fake_mp_por_categoria(cat),
            'categoria':        cat,
            'total':            len(canales),
            'peso_total':       round(sum(c.Peso or 0 for c in canales), 3),
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

        # ── Validación y armado de líneas ────────────────────────────────────
        lineas = []
        total_orden = 0.0

        for i, mp_id_raw in enumerate(mp_ids):
            num_linea = i + 1
            try:
                mp_id = int(mp_id_raw) if mp_id_raw else 0
            except ValueError:
                mp_id = 0

            cant_u    = _parse_int(cantidades_u[i]       if i < len(cantidades_u)     else '')
            cant_x    = _parse_int(cantidades_x[i]       if i < len(cantidades_x)     else '')
            precio    = _parse_float(precios[i]           if i < len(precios)          else '')
            fecha_cad = _parse_date(fechas_caducidad[i]   if i < len(fechas_caducidad)  else '')
            fecha_sac = _parse_date(fechas_sacrificio[i]  if i < len(fechas_sacrificio) else '')
            peso_c    = _parse_float(pesos_canal[i]       if i < len(pesos_canal)      else '')

            if not mp_id:
                flash(f'Línea {num_linea}: debes seleccionar la materia proveída.', 'danger')
                return redirect(url_for('compras.compra_nueva'))
            if cant_u <= 0:
                flash(f'Línea {num_linea}: la cantidad debe ser mayor a 0.', 'danger')
                return redirect(url_for('compras.compra_nueva'))
            if precio < 0:
                flash(f'Línea {num_linea}: el precio no puede ser negativo.', 'danger')
                return redirect(url_for('compras.compra_nueva'))

            mp_proveida = MateriaProveida.query.get(mp_id)
            if not mp_proveida or not mp_proveida.materiaPrima:
                flash(f'Línea {num_linea}: materia proveída inválida.', 'danger')
                return redirect(url_for('compras.compra_nueva'))

            materia = mp_proveida.materiaPrima
            tipo = materia.tipo or 'Materia'

            # ── Validaciones por tipo ────────────────────────────────────────
            if tipo == 'Canal':
                if materia.idCategoria is None:
                    flash(
                        f'Línea {num_linea}: la materia prima "{materia.nombreMateriaPrima}" '
                        f'es tipo Canal pero no tiene categoría asignada.',
                        'danger'
                    )
                    return redirect(url_for('compras.compra_nueva'))
                if not fecha_sac:
                    flash(f'Línea {num_linea} (Canal): la fecha de sacrificio es obligatoria.', 'danger')
                    return redirect(url_for('compras.compra_nueva'))
                if peso_c <= 0:
                    flash(f'Línea {num_linea} (Canal): el peso por canal debe ser mayor a 0.', 'danger')
                    return redirect(url_for('compras.compra_nueva'))

            elif tipo == 'Producto':
                if not materia.idProducto:
                    flash(
                        f'Línea {num_linea}: la materia prima "{materia.nombreMateriaPrima}" '
                        f'es tipo Producto pero no tiene un producto vinculado.',
                        'danger'
                    )
                    return redirect(url_for('compras.compra_nueva'))
                if cant_x <= 0:
                    flash(f'Línea {num_linea}: la cantidad por unidad debe ser mayor a 0.', 'danger')
                    return redirect(url_for('compras.compra_nueva'))
                if not fecha_cad:
                    flash(f'Línea {num_linea} (Producto): la fecha de caducidad es obligatoria.', 'danger')
                    return redirect(url_for('compras.compra_nueva'))

            elif tipo == 'Materia':
                if cant_x <= 0:
                    flash(f'Línea {num_linea}: la cantidad por unidad debe ser mayor a 0.', 'danger')
                    return redirect(url_for('compras.compra_nueva'))
                if not fecha_cad:
                    flash(f'Línea {num_linea} (Materia): la fecha de caducidad es obligatoria.', 'danger')
                    return redirect(url_for('compras.compra_nueva'))

            else:
                flash(
                    f'Línea {num_linea}: tipo de materia prima desconocido ("{tipo}"). '
                    f'Se omitió la línea.',
                    'warning'
                )
                continue

            total_costo  = cant_u * precio
            total_materia = cant_u * cant_x
            total_orden += total_costo
            lineas.append((mp_proveida, materia, tipo, cant_u, cant_x, precio,
                           total_costo, total_materia, fecha_cad, fecha_sac, peso_c))

        if not lineas:
            flash('No hay líneas válidas para registrar la orden.', 'danger')
            return redirect(url_for('compras.compra_nueva'))

        # ── Crear la orden de compra ─────────────────────────────────────────
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

        for (mp_proveida, materia, tipo, cant_u, cant_x, precio,
             total_costo, total_materia, fecha_cad, fecha_sac, peso_c) in lineas:

            # ── Tipo Producto → producto_unitario ────────────────────────────
            if tipo == 'Producto':
                n_piezas = max(1, int(round(cant_u * (cant_x or 1))))
                for _ in range(n_piezas):
                    pu = ProductoUnitario(
                        idProducto     = materia.idProducto,
                        idOrdenCompra  = orden.idOrdenCompra,
                        NumeroLote     = numero_lote,
                        FechaCaducidad = fecha_cad,
                        estatus        = estatus_item,
                    )
                    db.session.add(pu)

            # ── Tipo Canal → canal + canal_corte (auto) ──────────────────────
            elif tipo == 'Canal':
                n_canales = max(1, int(round(cant_u)))
                for _ in range(n_canales):
                    canal = Canal(
                        idCategoria     = materia.idCategoria,
                        idOrdenCompra   = orden.idOrdenCompra,
                        Descripcion     = materia.nombreMateriaPrima,
                        Peso            = peso_c if peso_c else None,
                        fechaSacrificio = fecha_sac,
                        estatus         = estatus_item,
                    )
                    db.session.add(canal)
                    db.session.flush()  # necesitamos canal.idCanal antes de crear los canal_corte
                    _crear_canal_cortes_para(canal)

            # ── Tipo Materia → lote (compra directa de materia prima) ────────
            elif tipo == 'Materia':
                lote = Lote(
                    idOrdenCompra     = orden.idOrdenCompra,
                    idMateriaProveida = mp_proveida.idMateriaProveida,
                    idCanalCorte      = None,
                    numeroLote        = numero_lote,
                    cantidadDeUnidad  = cant_u,
                    cantidadPorUnidad = float(cant_x),
                    totalMateria      = float(total_materia),
                    precioPorUnidad   = precio,
                    totalCosto        = round(total_costo, 2),
                    fechaCaducidad    = fecha_cad,
                    estatus           = estatus_item,
                )
                db.session.add(lote)

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

        # Lotes de materia prima en espera
        for lote in Lote.query.filter_by(
            idOrdenCompra=orden.idOrdenCompra, estatus='EnEspera'
        ).all():
            lote.estatus = 'Disponible'

        # Productos unitarios en espera
        for pu in ProductoUnitario.query.filter_by(
            idOrdenCompra=orden.idOrdenCompra, estatus='EnEspera'
        ).all():
            pu.estatus = 'Disponible'

        # Canales en espera
        for canal in Canal.query.filter_by(
            idOrdenCompra=orden.idOrdenCompra, estatus='EnEspera'
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

        # Lotes de materia prima en espera
        for lote in Lote.query.filter_by(
            idOrdenCompra=orden.idOrdenCompra, estatus='EnEspera'
        ).all():
            lote.estatus = 'Cancelado'

        # Productos unitarios en espera → Desechado
        for pu in ProductoUnitario.query.filter_by(
            idOrdenCompra=orden.idOrdenCompra, estatus='EnEspera'
        ).all():
            pu.estatus = 'Desechado'

        # Canales en espera → Cancelado
        for canal in Canal.query.filter_by(
            idOrdenCompra=orden.idOrdenCompra, estatus='EnEspera'
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

    # Lotes de materia prima
    items = Lote.query.filter_by(idOrdenCompra=orden.idOrdenCompra).all()

    # Resumen de productos unitarios
    pu_lista = ProductoUnitario.query.filter_by(idOrdenCompra=orden.idOrdenCompra).all()
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

    # Resumen de canales por categoría
    canal_lista = Canal.query.filter_by(idOrdenCompra=orden.idOrdenCompra).all()
    canal_por_cat = defaultdict(list)
    for c in canal_lista:
        canal_por_cat[c.idCategoria].append(c)
    items_canal = [
        {
            'materia_proveida': _fake_mp_por_categoria(Categoria.query.get(id_cat)),
            'categoria':        Categoria.query.get(id_cat),
            'total':            len(canales),
            'peso_total':       round(sum(c.Peso or 0 for c in canales), 3),
            'fecha_sacrificio': canales[0].fechaSacrificio,
        }
        for id_cat, canales in canal_por_cat.items()
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
    Devuelve unidad, conversor y tipo de la materia prima.
    El campo tipo es usado por el frontend para mostrar campos condicionales
    (fecha_caducidad para Materia/Producto, fecha_sacrificio + peso para Canal).
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
