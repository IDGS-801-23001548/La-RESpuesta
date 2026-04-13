from flask import render_template, redirect, url_for, flash, request, jsonify
from . import venta
from app.extensions import db, mongo_fotos
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.producto_unitario import ProductoUnitario
from app.models.carrito import Carrito
from app.models.pedido import Pedido
from app.models.corte import Corte
from app.models.corte_unitario import CorteUnitario
from app.models.canal_corte import CanalCorte
from app.models.lote import Lote
from app.modules.venta.forms import AgregarAlCarritoForm
from flask_security import login_required
from flask_login import current_user
from flask_wtf.csrf import validate_csrf, ValidationError


# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════

def _get_or_create_carrito():
    """Devuelve el carrito activo del usuario; lo crea si no existe."""
    carrito = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito:
        carrito = Carrito(idUsuario=current_user.id)
        db.session.add(carrito)
        db.session.commit()
    return carrito


def _carrito_count():
    """Cantidad total de items en el carrito (productos + cortes)."""
    carrito = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito:
        return 0
    n_productos = carrito.productos.filter_by(estatus='EnCarrito').count()
    n_cortes    = carrito.cortes.filter_by(estatus='EnCarrito').count()
    return n_productos + n_cortes


def _agrupar_unidades(unidades):
    """
    Recibe una lista de ProductoUnitario y devuelve una lista de dicts agrupados
    por producto: [{ producto, cantidad, subtotal_con_iva, ultima_unidad_id }, ...]
    Los precios YA incluyen IVA (precio de venta = precio final con impuesto incluido).
    """
    resumen = {}
    for u in unidades:
        pid = u.idProducto
        if pid not in resumen:
            resumen[pid] = {
                'producto':         u.producto,
                'cantidad':         0,
                'subtotal':         0.0,
                'ultima_unidad_id': u.idProductoUnitario
            }
        resumen[pid]['cantidad'] += 1
        resumen[pid]['subtotal'] += u.producto.PrecioVentaProducto
        resumen[pid]['ultima_unidad_id'] = u.idProductoUnitario
    return list(resumen.values())


def _agrupar_cortes(cortes_unitarios):
    """
    Recibe una lista de CorteUnitario y devuelve una lista de dicts:
    [{ corte, peso, costo, id_corte_unitario, foto_b64 }, ...]
    Cada CorteUnitario es un item individual (no se agrupan porque cada uno
    puede tener peso diferente).
    """
    items = []
    for cu in cortes_unitarios:
        foto = _foto_b64(cu.corte.idFoto) if cu.corte else None
        cat = cu.corte.categoria if cu.corte else None
        items.append({
            'corte_unitario': cu,
            'corte':          cu.corte,
            'nombre':         cu.corte.nombreCorte if cu.corte else '—',
            'categoria':      cat.nombreCategoria if cat else '—',
            'peso':           cu.peso,
            'costo':          cu.costo,
            'foto_b64':       foto,
        })
    return items


def _calcular_totales(items_productos, items_cortes=None):
    """
    Calcula el desglose a partir del total CON IVA incluido.
    En Mexico el precio de venta ya incluye IVA (16%).
    total_con_iva  = precio de venta (lo que paga el cliente)
    base_sin_iva   = total / 1.16
    iva_desglosado = total - base_sin_iva
    """
    total_productos = sum(i['subtotal'] for i in items_productos)
    total_cortes    = sum(i['costo'] for i in (items_cortes or []))
    total_con_iva   = round(total_productos + total_cortes, 2)
    base_sin_iva    = round(total_con_iva / 1.16, 2)
    iva_desglosado  = round(total_con_iva - base_sin_iva, 2)
    return total_con_iva, base_sin_iva, iva_desglosado


def _foto_b64(id_foto):
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


EMOJI_MAP = {
    'Res':     '🐄',
    'Cerdo':   '🐷',
    'Pollo':   '🐔',
    'Borrego': '🐑',
}

COLOR_MAP = {
    'Res':     'red',
    'Cerdo':   'pink',
    'Pollo':   'amber',
    'Borrego': 'purple',
}


def _enrich_productos_con_fotos(productos, categorias_map=None):
    """
    Recibe una lista de objetos Producto (SQLAlchemy) y devuelve una lista
    de dicts enriquecidos con la foto en base64 obtenida de MongoDB y datos
    de categoria para usar en filtros.
    """
    resultado = []
    for p in productos:
        foto_b64 = _foto_b64(p.idFoto)

        cat_nombre = '—'
        cat_filtro = 'sin'
        if categorias_map and p.idCategoria and p.idCategoria in categorias_map:
            cat_nombre = categorias_map[p.idCategoria]
            cat_filtro = str(p.idCategoria)

        resultado.append({
            'producto':   p,
            'foto_b64':   foto_b64,
            'cat_nombre': cat_nombre,
            'cat_filtro': cat_filtro,
        })
    return resultado


def _buscar_lote_fifo(id_corte):
    """Busca el primer lote disponible (FIFO por caducidad) para un corte dado.
    Camino: Corte → CanalCorte → Lote donde estatus = 'Disponible' y totalMateria > 0.
    Ordena por fechaCaducidad ASC (nulls last), idLote ASC.
    """
    return (
        Lote.query
        .join(CanalCorte, Lote.idCanalCorte == CanalCorte.idCanalCorte)
        .filter(
            CanalCorte.idCorte == id_corte,
            Lote.estatus == 'Disponible',
            Lote.totalMateria > 0,
        )
        .order_by(
            Lote.fechaCaducidad.is_(None),
            Lote.fechaCaducidad.asc(),
            Lote.idLote.asc(),
        )
        .first()
    )


def _stock_disponible_corte(id_corte):
    """Suma total de kg disponibles en lotes para un corte."""
    from sqlalchemy import func
    total = (
        db.session.query(func.coalesce(func.sum(Lote.totalMateria), 0))
        .join(CanalCorte, Lote.idCanalCorte == CanalCorte.idCanalCorte)
        .filter(
            CanalCorte.idCorte == id_corte,
            Lote.estatus == 'Disponible',
            Lote.totalMateria > 0,
        )
        .scalar()
    )
    return float(total or 0)


# ═══════════════════════════════════════════════════════════════════
#  INICIO
# ═══════════════════════════════════════════════════════════════════

@venta.route("/inicio", methods=['GET'])
@login_required
def inicio():
    pedidos_activos = Pedido.query.filter_by(
        idUsuario=current_user.id,
        Estatus='EnCurso'
    ).count()

    return render_template(
        "venta/ventasIndex.html",
        pedidos_activos=pedidos_activos,
        carrito_count=_carrito_count()
    )


# ═══════════════════════════════════════════════════════════════════
#  CATALOGO DE PRODUCTOS (unidades)
# ═══════════════════════════════════════════════════════════════════

@venta.route("/catalogo", methods=['GET'])
@login_required
def catalogo():
    form = AgregarAlCarritoForm()

    productos_db = (Producto.query
                    .filter(Producto.StockProducto > 0)
                    .order_by(Producto.NombreProducto)
                    .all())

    categorias_map = {c.idCategoria: c.nombreCategoria for c in Categoria.query.all()}
    items = _enrich_productos_con_fotos(productos_db, categorias_map=categorias_map)

    precios    = [i['producto'].PrecioVentaProducto for i in items]
    precio_min = int(min(precios)) if precios else 0
    precio_max = int(max(precios)) if precios else 9999

    categorias_lista = Categoria.query.order_by(Categoria.nombreCategoria).all()

    return render_template(
        "venta/catalogo.html",
        items=items,
        precio_min=precio_min,
        precio_max=precio_max,
        categorias_lista=categorias_lista,
        emoji_map=EMOJI_MAP,
        color_map=COLOR_MAP,
        form=form,
        carrito_count=_carrito_count(),
    )


# ═══════════════════════════════════════════════════════════════════
#  CATALOGO DE CORTES (peso/kg)
# ═══════════════════════════════════════════════════════════════════

@venta.route("/catalogo_cortes", methods=['GET'])
@login_required
def catalogo_cortes():
    """Catalogo de cortes disponibles para venta por peso."""
    form = AgregarAlCarritoForm()

    # Obtener cortes que tienen precio y al menos un lote disponible
    cortes_db = Corte.query.filter(
        Corte.precioPorKilo > 0,
    ).order_by(Corte.nombreCorte).all()

    categorias_map = {c.idCategoria: c.nombreCategoria for c in Categoria.query.all()}

    items = []
    for c in cortes_db:
        stock_kg = _stock_disponible_corte(c.idCorte)
        if stock_kg <= 0:
            continue  # Solo mostrar cortes con stock real

        foto = _foto_b64(c.idFoto)
        cat = categorias_map.get(c.idCategoria, '—')
        items.append({
            'corte':       c,
            'foto_b64':    foto,
            'cat_nombre':  cat,
            'cat_filtro':  str(c.idCategoria) if c.idCategoria else 'sin',
            'stock_kg':    round(stock_kg, 2),
        })

    categorias_lista = Categoria.query.order_by(Categoria.nombreCategoria).all()

    return render_template(
        "venta/catalogo_cortes.html",
        items=items,
        categorias_lista=categorias_lista,
        emoji_map=EMOJI_MAP,
        color_map=COLOR_MAP,
        form=form,
        carrito_count=_carrito_count(),
    )


# ═══════════════════════════════════════════════════════════════════
#  REDIRECTS LEGACY
# ═══════════════════════════════════════════════════════════════════

@venta.route("/seleccionar_animal", methods=['GET'])
@login_required
def seleccionar_animal():
    return redirect(url_for('venta.catalogo'))


@venta.route("/catalogo_res", methods=['GET'])
@login_required
def catalogo_res():
    return redirect(url_for('venta.catalogo'))


@venta.route("/catalogo_cerdo", methods=['GET'])
@login_required
def catalogo_cerdo():
    return redirect(url_for('venta.catalogo'))


@venta.route("/catalogo_pollo", methods=['GET'])
@login_required
def catalogo_pollo():
    return redirect(url_for('venta.catalogo'))


@venta.route("/catalogo_borrego", methods=['GET'])
@login_required
def catalogo_borrego():
    return redirect(url_for('venta.catalogo'))


# ═══════════════════════════════════════════════════════════════════
#  CARRITO — AGREGAR PRODUCTO (unidad)
# ═══════════════════════════════════════════════════════════════════

@venta.route("/carrito/agregar/<int:id_producto>", methods=['POST'])
@login_required
def agregar_al_carrito(id_producto):
    form = AgregarAlCarritoForm()
    if not form.validate_on_submit():
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'Token CSRF invalido'}), 400
        flash('Solicitud invalida.', 'error')
        return redirect(request.referrer or url_for('venta.catalogo'))

    try:
        cantidad = int(request.form.get('cantidad') or 1)
    except ValueError:
        cantidad = 1
    cantidad = max(1, cantidad)

    producto    = Producto.query.get_or_404(id_producto)
    carrito_obj = _get_or_create_carrito()

    unidades_disponibles = (ProductoUnitario.query
                            .filter_by(idProducto=id_producto, estatus='Disponible')
                            .limit(cantidad)
                            .all())

    if not unidades_disponibles:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'Sin stock disponible'}), 400
        flash('No hay unidades disponibles de ese producto.', 'warning')
        return redirect(request.referrer or url_for('venta.catalogo'))

    for u in unidades_disponibles:
        u.estatus   = 'EnCarrito'
        u.idCarrito = carrito_obj.idCarrito
    db.session.commit()

    n = len(unidades_disponibles)
    msg = f'{n} x "{producto.NombreProducto}" agregado(s) al carrito'
    if n < cantidad:
        msg += f' (solo habia {n} disponibles)'

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'ok':            True,
            'carrito_count': _carrito_count(),
            'agregados':     n,
            'msg':           msg,
        })

    flash(msg, 'success')
    return redirect(request.referrer or url_for('venta.carrito'))


# ═══════════════════════════════════════════════════════════════════
#  CARRITO — AGREGAR CORTE (peso/kg)
# ═══════════════════════════════════════════════════════════════════

@venta.route("/carrito/agregar_corte/<int:id_corte>", methods=['POST'])
@login_required
def agregar_corte_al_carrito(id_corte):
    """Agrega un corte al carrito por peso. Descuenta FIFO del lote."""
    form = AgregarAlCarritoForm()
    if not form.validate_on_submit():
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'Token CSRF invalido'}), 400
        flash('Solicitud invalida.', 'error')
        return redirect(request.referrer or url_for('venta.catalogo_cortes'))

    try:
        peso = float(request.form.get('peso', 0))
    except (TypeError, ValueError):
        peso = 0

    if peso <= 0:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'El peso debe ser mayor a 0'}), 400
        flash('Debes indicar un peso mayor a 0.', 'warning')
        return redirect(request.referrer or url_for('venta.catalogo_cortes'))

    corte_obj = Corte.query.get_or_404(id_corte)
    if not corte_obj.precioPorKilo or corte_obj.precioPorKilo <= 0:
        flash('Este corte no tiene precio asignado.', 'warning')
        return redirect(request.referrer or url_for('venta.catalogo_cortes'))

    # Buscar lote FIFO
    lote = _buscar_lote_fifo(id_corte)
    if not lote:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'Sin stock disponible'}), 400
        flash('No hay lotes disponibles para este corte.', 'warning')
        return redirect(request.referrer or url_for('venta.catalogo_cortes'))

    # Verificar stock suficiente en el lote
    if (lote.totalMateria or 0) < peso:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': f'Stock insuficiente. Disponible: {lote.totalMateria:.2f} kg'}), 400
        flash(f'Stock insuficiente. Disponible: {lote.totalMateria:.2f} kg.', 'warning')
        return redirect(request.referrer or url_for('venta.catalogo_cortes'))

    # Descontar del lote
    costo = round(corte_obj.precioPorKilo * peso, 2)
    lote.totalMateria = round((lote.totalMateria or 0) - peso, 3)
    if lote.totalMateria <= 0:
        lote.totalMateria = 0
        lote.estatus = 'Agotado'

    # Crear registro
    carrito_obj = _get_or_create_carrito()
    nuevo_cu = CorteUnitario(
        idCorte   = corte_obj.idCorte,
        idLote    = lote.idLote,
        idCarrito = carrito_obj.idCarrito,
        idPedido  = None,
        peso      = peso,
        costo     = costo,
        estatus   = 'EnCarrito',
    )
    db.session.add(nuevo_cu)
    db.session.commit()

    msg = f'{peso:.2f} kg de "{corte_obj.nombreCorte}" agregado al carrito (${costo:.2f})'

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'ok':            True,
            'carrito_count': _carrito_count(),
            'msg':           msg,
        })

    flash(msg, 'success')
    return redirect(request.referrer or url_for('venta.carrito'))


# ═══════════════════════════════════════════════════════════════════
#  CARRITO — QUITAR PRODUCTO (unidad)
# ═══════════════════════════════════════════════════════════════════

@venta.route("/carrito/quitar/<int:id_producto_unitario>", methods=['POST'])
@login_required
def quitar_del_carrito(id_producto_unitario):
    """Devuelve una unidad al stock (estado Disponible)."""
    form = AgregarAlCarritoForm()

    if not form.validate_on_submit():
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'Token CSRF invalido'}), 400
        flash('Solicitud invalida (CSRF).', 'error')
        return redirect(url_for('venta.carrito'))

    unidad      = ProductoUnitario.query.get_or_404(id_producto_unitario)
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()

    if not carrito_obj or unidad.idCarrito != carrito_obj.idCarrito:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'No autorizado'}), 403
        flash('No puedes modificar ese carrito.', 'error')
        return redirect(url_for('venta.carrito'))

    unidad.estatus   = 'Disponible'
    unidad.idCarrito = None
    db.session.commit()

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'ok': True, 'carrito_count': _carrito_count()})

    flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('venta.carrito'))


# ═══════════════════════════════════════════════════════════════════
#  CARRITO — QUITAR CORTE
# ═══════════════════════════════════════════════════════════════════

@venta.route("/carrito/quitar_corte/<int:id_corte_unitario>", methods=['POST'])
@login_required
def quitar_corte_del_carrito(id_corte_unitario):
    """Devuelve el peso al lote y elimina el CorteUnitario del carrito."""
    form = AgregarAlCarritoForm()

    if not form.validate_on_submit():
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'Token CSRF invalido'}), 400
        flash('Solicitud invalida (CSRF).', 'error')
        return redirect(url_for('venta.carrito'))

    cu = CorteUnitario.query.get_or_404(id_corte_unitario)
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()

    if not carrito_obj or cu.idCarrito != carrito_obj.idCarrito:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': False, 'msg': 'No autorizado'}), 403
        flash('No puedes modificar ese carrito.', 'error')
        return redirect(url_for('venta.carrito'))

    # Devolver peso al lote
    if cu.idLote:
        lote = Lote.query.get(cu.idLote)
        if lote:
            lote.totalMateria = round((lote.totalMateria or 0) + cu.peso, 3)
            if lote.estatus == 'Agotado':
                lote.estatus = 'Disponible'

    db.session.delete(cu)
    db.session.commit()

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'ok': True, 'carrito_count': _carrito_count()})

    flash('Corte eliminado del carrito.', 'success')
    return redirect(url_for('venta.carrito'))


# ═══════════════════════════════════════════════════════════════════
#  CARRITO — VACIAR-TODO
# ═══════════════════════════════════════════════════════════════════

@venta.route("/carrito/vaciar", methods=['POST'])
@login_required
def vaciar_carrito():
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if carrito_obj:
        # Devolver productos
        for u in carrito_obj.productos.filter_by(estatus='EnCarrito').all():
            u.estatus   = 'Disponible'
            u.idCarrito = None

        # Devolver cortes (peso al lote)
        for cu in carrito_obj.cortes.filter_by(estatus='EnCarrito').all():
            if cu.idLote:
                lote = Lote.query.get(cu.idLote)
                if lote:
                    lote.totalMateria = round((lote.totalMateria or 0) + cu.peso, 3)
                    if lote.estatus == 'Agotado':
                        lote.estatus = 'Disponible'
            db.session.delete(cu)

        db.session.commit()

    flash('Carrito vaciado.', 'success')
    return redirect(url_for('venta.catalogo'))


# ═══════════════════════════════════════════════════════════════════
#  CARRITO — VER
# ═══════════════════════════════════════════════════════════════════

@venta.route("/carrito", methods=['GET'])
@login_required
def carrito():
    carrito_obj = _get_or_create_carrito()

    # Productos
    unidades       = carrito_obj.productos.filter_by(estatus='EnCarrito').all()
    items_productos = _agrupar_unidades(unidades)

    # Cortes
    cortes_en_carrito = carrito_obj.cortes.filter_by(estatus='EnCarrito').all()
    items_cortes      = _agrupar_cortes(cortes_en_carrito)

    total_con_iva, base_sin_iva, iva_desglosado = _calcular_totales(items_productos, items_cortes)

    # Direccion del usuario para mostrar como sugerencia en el carrito
    direccion_usuario = ''
    if current_user.persona and current_user.persona.direccion:
        direccion_usuario = current_user.persona.direccion

    form = AgregarAlCarritoForm()

    return render_template(
        "venta/carrito.html",
        items=items_productos,
        items_cortes=items_cortes,
        base_sin_iva=base_sin_iva,
        iva=iva_desglosado,
        total=total_con_iva,
        carrito_count=len(unidades) + len(cortes_en_carrito),
        direccion_usuario=direccion_usuario,
        form=form
    )


# ═══════════════════════════════════════════════════════════════════
#  PAGO — VER
# ═══════════════════════════════════════════════════════════════════

@venta.route("/pago", methods=['GET'])
@login_required
def pago():
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito_obj:
        flash('Tu carrito esta vacio.', 'warning')
        return redirect(url_for('venta.catalogo'))

    unidades = carrito_obj.productos.filter_by(estatus='EnCarrito').all()
    cortes   = carrito_obj.cortes.filter_by(estatus='EnCarrito').all()

    if not unidades and not cortes:
        flash('Tu carrito esta vacio.', 'warning')
        return redirect(url_for('venta.catalogo'))

    items_productos = _agrupar_unidades(unidades)
    items_cortes    = _agrupar_cortes(cortes)
    total_con_iva, base_sin_iva, iva_desglosado = _calcular_totales(items_productos, items_cortes)

    # Direccion por defecto del usuario
    direccion_default = ''
    if current_user.persona and current_user.persona.direccion:
        direccion_default = current_user.persona.direccion

    form = AgregarAlCarritoForm()

    return render_template(
        "venta/pago.html",
        items=items_productos,
        items_cortes=items_cortes,
        base_sin_iva=base_sin_iva,
        iva=iva_desglosado,
        total=total_con_iva,
        carrito_count=len(unidades) + len(cortes),
        direccion_default=direccion_default,
        form=form
    )


# ═══════════════════════════════════════════════════════════════════
#  PAGO — CONFIRMAR  (crea el Pedido)
# ═══════════════════════════════════════════════════════════════════

@venta.route("/pago/confirmar", methods=['POST'])
@login_required
def confirmar_pago():
    form = AgregarAlCarritoForm()
    if not form.validate_on_submit():
        flash('Solicitud invalida (CSRF).', 'error')
        return redirect(url_for('venta.pago'))

    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito_obj:
        flash('Tu carrito esta vacio.', 'warning')
        return redirect(url_for('venta.carrito'))

    unidades = carrito_obj.productos.filter_by(estatus='EnCarrito').all()
    cortes   = carrito_obj.cortes.filter_by(estatus='EnCarrito').all()

    if not unidades and not cortes:
        flash('Tu carrito esta vacio.', 'warning')
        return redirect(url_for('venta.carrito'))

    metodo_pago  = request.form.get('metodo_pago', 'Tarjeta')
    tipo_entrega = request.form.get('tipo_entrega', 'Domicilio')

    # Direccion especifica de este pedido
    direccion_pedido = request.form.get('direccion_pedido', '').strip()
    if not direccion_pedido and current_user.persona:
        direccion_pedido = current_user.persona.direccion or ''

    # Notas del pedido
    notas_pedido = request.form.get('notas', '').strip()

    # Calcular total
    items_productos = _agrupar_unidades(unidades)
    items_cortes    = _agrupar_cortes(cortes)
    total_con_iva, _, _ = _calcular_totales(items_productos, items_cortes)

    nuevo_pedido = Pedido(
        idUsuario=current_user.id,
        Total=total_con_iva,
        Tipo=metodo_pago,
        Estatus='EnCurso',
        Entrega=tipo_entrega,
        Direccion=direccion_pedido,
        Notas=notas_pedido
    )
    db.session.add(nuevo_pedido)
    db.session.flush()  # obtiene idPedido antes del commit

    # Mover productos
    for u in unidades:
        u.estatus   = 'Vendido'
        u.idCarrito = None
        u.idPedido  = nuevo_pedido.idPedido

    # Mover cortes
    for cu in cortes:
        cu.estatus   = 'Vendido'
        cu.idCarrito = None
        cu.idPedido  = nuevo_pedido.idPedido

    db.session.commit()

    flash(f'Pedido #VO-{nuevo_pedido.idPedido:04d} confirmado exitosamente!', 'success')
    return redirect(url_for('venta.pedido_detalle', id_pedido=nuevo_pedido.idPedido))


# ═══════════════════════════════════════════════════════════════════
#  PEDIDOS — LISTA
# ═══════════════════════════════════════════════════════════════════

@venta.route("/pedidos", methods=['GET'])
@login_required
def pedidos():
    filtro = request.args.get('estatus', 'todos')

    query = Pedido.query.filter_by(idUsuario=current_user.id)
    if filtro == 'en_curso':
        query = query.filter_by(Estatus='EnCurso')
    elif filtro == 'finalizados':
        query = query.filter_by(Estatus='Finalizado')
    elif filtro == 'cancelados':
        query = query.filter_by(Estatus='Cancelado')

    mis_pedidos   = query.order_by(Pedido.idPedido.desc()).all()
    total_pedidos = Pedido.query.filter_by(idUsuario=current_user.id).count()
    en_curso      = Pedido.query.filter_by(idUsuario=current_user.id, Estatus='EnCurso').count()
    finalizados   = Pedido.query.filter_by(idUsuario=current_user.id, Estatus='Finalizado').count()
    cancelados    = Pedido.query.filter_by(idUsuario=current_user.id, Estatus='Cancelado').count()

    return render_template(
        "venta/pedidos.html",
        pedidos=mis_pedidos,
        filtro_activo=filtro,
        total_pedidos=total_pedidos,
        en_curso=en_curso,
        finalizados=finalizados,
        cancelados=cancelados,
        carrito_count=_carrito_count()
    )


# ═══════════════════════════════════════════════════════════════════
#  PEDIDOS — DETALLE
# ═══════════════════════════════════════════════════════════════════

@venta.route("/pedido/<int:id_pedido>", methods=['GET'])
@login_required
def pedido_detalle(id_pedido):
    pedido = Pedido.query.filter_by(
        idPedido=id_pedido,
        idUsuario=current_user.id
    ).first_or_404()

    items_productos = _agrupar_unidades(pedido.unidadesPedido.all())
    items_cortes    = _agrupar_cortes(pedido.cortesPedido.all())
    total_con_iva, base_sin_iva, iva_desglosado = _calcular_totales(items_productos, items_cortes)

    pasos = {
        'EnCurso':    ['done', 'done', 'active', 'pending'],
        'Finalizado': ['done', 'done', 'done',   'done'],
        'Cancelado':  ['done', 'pending', 'pending', 'pending'],
    }
    timeline = pasos.get(pedido.Estatus, ['done', 'pending', 'pending', 'pending'])

    return render_template(
        "venta/pedido_detalle.html",
        pedido=pedido,
        items=items_productos,
        items_cortes=items_cortes,
        base_sin_iva=base_sin_iva,
        iva=iva_desglosado,
        total=pedido.Total,
        timeline=timeline,
        carrito_count=_carrito_count()
    )


# ═══════════════════════════════════════════════════════════════════
#  PEDIDOS — CANCELAR
# ═══════════════════════════════════════════════════════════════════

@venta.route("/pedido/<int:id_pedido>/cancelar", methods=['POST'])
@login_required
def cancelar_pedido(id_pedido):
    pedido = Pedido.query.filter_by(
        idPedido=id_pedido,
        idUsuario=current_user.id
    ).first_or_404()

    if pedido.Estatus != 'EnCurso':
        flash('Solo puedes cancelar pedidos que esten en curso.', 'warning')
        return redirect(url_for('venta.pedido_detalle', id_pedido=id_pedido))

    # Devolver productos
    for u in pedido.unidadesPedido.all():
        u.estatus  = 'Disponible'
        u.idPedido = None

    # Devolver cortes (peso al lote)
    for cu in pedido.cortesPedido.all():
        if cu.idLote:
            lote = Lote.query.get(cu.idLote)
            if lote:
                lote.totalMateria = round((lote.totalMateria or 0) + cu.peso, 3)
                if lote.estatus == 'Agotado':
                    lote.estatus = 'Disponible'
        cu.estatus  = 'Cancelado'
        cu.idPedido = None

    pedido.Estatus = 'Cancelado'
    db.session.commit()

    flash(f'Pedido #VO-{id_pedido:04d} cancelado. Los productos volvieron al inventario.', 'success')
    return redirect(url_for('venta.pedidos'))


# ═══════════════════════════════════════════════════════════════════
#  PEDIDOS — TICKET
# ═══════════════════════════════════════════════════════════════════

@venta.route("/pedido/<int:id_pedido>/ticket", methods=['GET'])
@login_required
def ticket_pedido(id_pedido):
    pedido = Pedido.query.filter_by(
        idPedido=id_pedido,
        idUsuario=current_user.id
    ).first_or_404()

    items_productos = _agrupar_unidades(pedido.unidadesPedido.all())
    items_cortes    = _agrupar_cortes(pedido.cortesPedido.all())
    total_con_iva, base_sin_iva, iva_desglosado = _calcular_totales(items_productos, items_cortes)

    return render_template(
        "venta/ticket_pedido.html",
        pedido=pedido,
        items=items_productos,
        items_cortes=items_cortes,
        base_sin_iva=base_sin_iva,
        iva=iva_desglosado,
        total=pedido.Total,
        carrito_count=_carrito_count()
    )


# ═══════════════════════════════════════════════════════════════════
#  AJUSTES — VER
# ═══════════════════════════════════════════════════════════════════

@venta.route("/ajustes", methods=['GET'])
@login_required
def ajustes():
    return render_template(
        "venta/ajustes.html",
        carrito_count=_carrito_count()
    )


# ═══════════════════════════════════════════════════════════════════
#  AJUSTES — GUARDAR DATOS PERSONALES
# ═══════════════════════════════════════════════════════════════════

@venta.route("/ajustes/datos", methods=['POST'])
@login_required
def ajustes_datos():
    try:
        validate_csrf(request.form.get('csrf_token'))
    except ValidationError:
        flash('Solicitud invalida (CSRF).', 'error')
        return redirect(url_for('venta.ajustes'))

    nombre           = request.form.get('nombre', '').strip()
    apellido         = request.form.get('apellido', '').strip()
    apellido_materno = request.form.get('apellido_materno', '').strip()
    email            = request.form.get('email', '').strip()
    telefono         = request.form.get('telefono', '').strip()
    direccion        = request.form.get('direccion', '').strip()

    if not nombre or not email:
        flash('Nombre y correo son obligatorios.', 'error')
        return redirect(url_for('venta.ajustes'))

    current_user.email = email

    persona = current_user.persona
    if not persona:
        from app.models.persona import Persona
        persona = Persona(user_id=current_user.id)
        db.session.add(persona)

    persona.nombre           = nombre
    persona.apellido_paterno = apellido
    persona.apellido_materno = apellido_materno
    persona.telefono         = telefono
    persona.direccion        = direccion

    db.session.commit()

    flash('Datos actualizados correctamente.', 'success')
    return redirect(url_for('venta.ajustes'))


# ═══════════════════════════════════════════════════════════════════
#  AJUSTES — CAMBIAR PASSWORD
# ═══════════════════════════════════════════════════════════════════

@venta.route("/ajustes/password", methods=['POST'])
@login_required
def ajustes_password():
    try:
        validate_csrf(request.form.get('csrf_token'))
    except ValidationError:
        flash('Solicitud invalida (CSRF).', 'error')
        return redirect(url_for('venta.ajustes'))

    from flask_security import verify_password
    from flask_security.utils import hash_password

    actual    = request.form.get('password_actual', '')
    nueva     = request.form.get('password_nueva', '')
    confirmar = request.form.get('password_confirmar', '')

    if not verify_password(actual, current_user.password):
        flash('La contrasena actual es incorrecta.', 'error')
        return redirect(url_for('venta.ajustes'))

    if len(nueva) < 8:
        flash('La nueva contrasena debe tener al menos 8 caracteres.', 'error')
        return redirect(url_for('venta.ajustes'))

    if nueva != confirmar:
        flash('Las contrasenas nuevas no coinciden.', 'error')
        return redirect(url_for('venta.ajustes'))

    current_user.password = hash_password(nueva)
    db.session.commit()

    flash('Contrasena actualizada correctamente.', 'success')
    return redirect(url_for('venta.ajustes'))
