from flask import render_template, redirect, url_for, flash, request, session, jsonify, current_app
from flask_login import login_required, current_user
from flask_security.decorators import roles_required
from . import mostrador
from datetime import datetime
import uuid
from app.extensions import db, mongo_fotos
from app.models.producto import Producto
from app.models.producto_unitario import ProductoUnitario
from app.models.pedido import Pedido
from app.models.ticket import Ticket
from app.models.vistaResumenPedido import VistaResumenPedido
from app.models.detallesTicket import DetalleTicket
from app.models.corte import Corte
from app.models.categoria import Categoria
from app.models.lote import Lote
from app.models.canal_corte import CanalCorte
from sqlalchemy import func
from app.models.corte_unitario import CorteUnitario
from .forms import (
    AgregarProductoForm,
    AgregarCorteForm,
    ModificarCantidadForm,
    EliminarProductoForm,
    VaciarCarritoForm,
    CobrarForm,
    EntregarPedidoForm
)


# ─── HELPERS ────────────────────────────────────────────────

def _normalizar_tickets(tickets):
    """Garantiza que todas las claves del dict sean strings."""
    return {str(k): v for k, v in tickets.items()}

def _get_ticket_activo():
    return str(session.get('ticket_activo', '1'))

def _get_tickets():
    raw = session.get('tickets', {'1': []})
    return _normalizar_tickets(raw)

def _save_tickets(tickets):
    session['tickets'] = _normalizar_tickets(tickets)
    session.modified = True

def _get_carrito_activo():
    tickets = _get_tickets()
    activo  = _get_ticket_activo()
    return list(tickets.get(activo, []))

def _save_carrito_activo(carrito):
    tickets = _get_tickets()
    activo  = _get_ticket_activo()
    tickets[activo] = carrito
    _save_tickets(tickets)

def _calcular_subtotal(item):
    return round(item['precio'] * item['cantidad'], 2)

def _build_carrito_from(carrito_raw):
    carrito_items = []
    total = 0.0
    for item in carrito_raw:
        subtotal = _calcular_subtotal(item)
        total   += subtotal
        carrito_items.append({**item, 'subtotal': subtotal})
    return carrito_items, round(total, 2)

def _build_carrito():
    return _build_carrito_from(_get_carrito_activo())


# ─── HELPERS DE FOTOS ───────────────────────────────────────

def _fetch_fotos_bulk(ids_foto):
    """
    Recibe una lista de idFoto (strings) y devuelve un dict
    {idFoto: data_uri} con UNA sola consulta a MongoDB.
    """
    if not ids_foto or mongo_fotos is None:
        return {}
    try:
        ids_str = [str(i) for i in ids_foto if i]
        docs = mongo_fotos.find(
            {'idFoto': {'$in': ids_str}},
            {'idFoto': 1, 'foto': 1, '_id': 0}   # solo los campos necesarios
        )
        resultado = {}
        for doc in docs:
            raw = doc.get('foto')
            if raw:
                if not raw.startswith('data:'):
                    raw = f'data:image/jpeg;base64,{raw}'
                resultado[doc['idFoto']] = raw
        return resultado
    except Exception:
        return {}


def _enrich_productos_con_fotos(productos):
    ids = [p.idFoto for p in productos if p.idFoto]
    fotos = _fetch_fotos_bulk(ids)
    return [
        {'producto': p, 'foto_b64': fotos.get(str(p.idFoto))}
        for p in productos
    ]


def _enrich_cortes_con_fotos(cortes_con_stock):
    ids = [e['corte'].idFoto for e in cortes_con_stock if e['corte'].idFoto]
    fotos = _fetch_fotos_bulk(ids)
    return [
        {
            'corte':    e['corte'],
            'stock_kg': e['stock_kg'],
            'foto_b64': fotos.get(str(e['corte'].idFoto)),
        }
        for e in cortes_con_stock
    ]


def _get_cortes_con_stock():
    """
    Devuelve todos los cortes junto con su stock_kg real,
    calculado como la suma de Lote.totalMateria de los lotes
    con estatus='Disponible' y totalMateria > 0, enlazados
    via CanalCorte.
    """
    from app.models.lote import Lote

    stock_sq = (
        db.session.query(
            CanalCorte.idCorte,
            func.coalesce(func.sum(Lote.totalMateria), 0.0).label('stock_kg')
        )
        .join(Lote, Lote.idCanalCorte == CanalCorte.idCanalCorte)
        .filter(
            Lote.estatus == 'Disponible',
            Lote.totalMateria > 0,
        )
        .group_by(CanalCorte.idCorte)
        .subquery()
    )

    rows = (
        db.session.query(Corte, func.coalesce(stock_sq.c.stock_kg, 0.0).label('stock_kg'))
        .outerjoin(stock_sq, Corte.idCorte == stock_sq.c.idCorte)
        .order_by(Corte.nombreCorte)
        .all()
    )

    return [{'corte': corte, 'stock_kg': round(float(stock_kg), 3)} for corte, stock_kg in rows]


# ─── CATÁLOGO DE CORTES (solo lectura) ──────────────────────

@mostrador.route("/catalogo-cortes", methods=['GET'])
@login_required
@roles_required('admin')
def catalogo_cortes():
    cortes_raw  = _get_cortes_con_stock()
    items_cortes = _enrich_cortes_con_fotos(cortes_raw)
    return render_template("mostrador/cortes_catalogo.html", items_cortes=items_cortes)


# ─── VISTA PRINCIPAL ────────────────────────────────────────

@mostrador.route("/venta", methods=['GET'])
@login_required
@roles_required('Cajero')
def mostradorVenta():
    if 'tickets' not in session:
        session['tickets'] = {'1': []}
        session['ticket_activo'] = '1'
        session.modified = True
    else:
        session['tickets'] = {str(k): v for k, v in session['tickets'].items()}
        session['ticket_activo'] = str(session.get('ticket_activo', '1'))
        session.modified = True

    # ── Productos normales ──
    productos      = Producto.query.order_by(Producto.NombreProducto).all()
    items_productos = _enrich_productos_con_fotos(productos)

    # ── Cortes con stock ──
    cortes_raw     = _get_cortes_con_stock()
    items_cortes   = _enrich_cortes_con_fotos(cortes_raw)

    # ── Carrito ──
    carrito_items, total = _build_carrito()
    tickets        = _get_tickets()
    ticket_activo  = _get_ticket_activo()

    # ── Forms ──
    agregar_form        = AgregarProductoForm()
    agregar_corte_form  = AgregarCorteForm()
    modificar_form      = ModificarCantidadForm()
    eliminar_form       = EliminarProductoForm()
    vaciar_form         = VaciarCarritoForm()
    cobrar_form         = CobrarForm()

    return render_template(
        "mostrador/mostrador.html",
        productos           = productos,
        items               = items_productos,
        items_cortes        = items_cortes,
        carrito             = carrito_items,
        total               = total,
        tickets             = tickets,
        ticket_activo       = ticket_activo,
        agregar_form        = agregar_form,
        agregar_corte_form  = agregar_corte_form,
        modificar_form      = modificar_form,
        eliminar_form       = eliminar_form,
        vaciar_form         = vaciar_form,
        cobrar_form         = cobrar_form,
    )


# ─── PRODUCTOS — AGREGAR ────────────────────────────────────

@mostrador.route("/venta/agregar/<int:id_producto>", methods=['POST'])
@login_required
@roles_required('Cajero')
def agregarProducto(id_producto):
    form = AgregarProductoForm()

    if not form.validate_on_submit():
        flash('Cantidad inválida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    cantidad = form.cantidad.data
    producto = Producto.query.get_or_404(id_producto)

    if producto.StockProducto <= 0:
        flash(f'"{producto.NombreProducto}" no tiene stock disponible.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito = _get_carrito_activo()

    for item in carrito:
        if item.get('id_producto') == id_producto and item.get('tipo') != 'corte':
            nueva_cantidad = round(item['cantidad'] + cantidad, 3)
            if nueva_cantidad > producto.StockProducto:
                flash(
                    f'Stock insuficiente. Máximo disponible: '
                    f'{producto.StockProducto} {item.get("unidad", "")}.',
                    'warning'
                )
                return redirect(url_for('mostrador.mostradorVenta'))
            item['cantidad'] = nueva_cantidad
            _save_carrito_activo(carrito)
            flash(f'"{producto.NombreProducto}" actualizado en el carrito.', 'success')
            return redirect(url_for('mostrador.mostradorVenta'))

    if cantidad > producto.StockProducto:
        flash(
            f'Stock insuficiente. Máximo disponible: {producto.StockProducto}.',
            'warning'
        )
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito.append({
        'tipo':        'producto',
        'id_producto': id_producto,
        'nombre':      producto.NombreProducto,
        'precio':      producto.PrecioVentaProducto,
        'cantidad':    round(cantidad, 3),
        'stock':       producto.StockProducto,
    })

    _save_carrito_activo(carrito)
    flash(f'"{producto.NombreProducto}" agregado al carrito.', 'success')
    return redirect(url_for('mostrador.mostradorVenta'))


# ─── CORTES — AGREGAR ───────────────────────────────────────

@mostrador.route("/venta/agregar-corte/<int:id_corte>", methods=['POST'])
@login_required
@roles_required('Cajero')
def agregarCorte(id_corte):
    form = AgregarCorteForm()

    if not form.validate_on_submit():
        flash('Peso inválido.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    peso   = round(form.peso.data, 3)
    corte  = Corte.query.get_or_404(id_corte)

    # Calcular stock actual
    stock_kg = db.session.query(
        func.coalesce(func.sum(Lote.totalMateria), 0.0)
        ).join(CanalCorte, Lote.idCanalCorte == CanalCorte.idCanalCorte
    ).filter(
        CanalCorte.idCorte == id_corte,
        Lote.estatus       == 'Disponible',
        Lote.totalMateria  > 0,
    ).scalar() or 0.0
    stock_kg = round(float(stock_kg), 3)

    if stock_kg <= 0:
        flash(f'"{corte.nombreCorte}" no tiene stock disponible.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito = _get_carrito_activo()

    # Clave única para cortes en el carrito
    for item in carrito:
        if item.get('tipo') == 'corte' and item.get('id_producto') == id_corte:
            nueva_cantidad = round(item['cantidad'] + peso, 3)
            if nueva_cantidad > stock_kg:
                flash(
                    f'Stock insuficiente. Máximo disponible: {stock_kg} kg.',
                    'warning'
                )
                return redirect(url_for('mostrador.mostradorVenta'))
            item['cantidad'] = nueva_cantidad
            item['stock']    = stock_kg
            _save_carrito_activo(carrito)
            flash(f'"{corte.nombreCorte}" actualizado en el carrito.', 'success')
            return redirect(url_for('mostrador.mostradorVenta'))

    if peso > stock_kg:
        flash(
            f'Stock insuficiente. Máximo disponible: {stock_kg} kg.',
            'warning'
        )
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito.append({
        'tipo':        'corte',
        'id_producto': id_corte,          # reutilizamos la clave para que el carrito funcione igual
        'nombre':      corte.nombreCorte,
        'precio':      corte.precioPorKilo,
        'cantidad':    peso,
        'stock':       stock_kg,
        'unidad':      'kg',
    })

    _save_carrito_activo(carrito)
    flash(f'"{corte.nombreCorte}" agregado al carrito.', 'success')
    return redirect(url_for('mostrador.mostradorVenta'))


# ─── MODIFICAR CANTIDAD ─────────────────────────────────────

@mostrador.route("/venta/modificar/<int:id_producto>", methods=['POST'])
@login_required
@roles_required('Cajero')
def modificarCantidad(id_producto):
    form = ModificarCantidadForm()

    if not form.validate_on_submit():
        flash('Cantidad inválida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    cantidad = form.cantidad.data
    accion   = request.form.get('accion')   # 'sumar' | 'restar' | None
    tipo     = request.form.get('tipo', 'producto')
    carrito  = _get_carrito_activo()

    # Paso para incremento: 1 para productos, 0.1 para cortes
    paso = 0.1 if tipo == 'corte' else 1

    for item in carrito:
        match = (
            item.get('id_producto') == id_producto and
            item.get('tipo', 'producto') == tipo
        )
        if not match:
            continue

        if accion == 'sumar':
            nueva_cantidad = round(cantidad + paso, 3)
        elif accion == 'restar':
            nueva_cantidad = round(cantidad - paso, 3)
        else:
            nueva_cantidad = round(cantidad, 3)

        if nueva_cantidad <= 0:
            carrito.remove(item)
            _save_carrito_activo(carrito)
            flash(f'"{item["nombre"]}" eliminado del carrito.', 'info')
            return redirect(url_for('mostrador.mostradorVenta'))

        if nueva_cantidad > item['stock']:
            flash(
                f'Stock insuficiente. Máximo: {item["stock"]}.',
                'warning'
            )
            return redirect(url_for('mostrador.mostradorVenta'))

        item['cantidad'] = round(nueva_cantidad, 3)
        _save_carrito_activo(carrito)
        return redirect(url_for('mostrador.mostradorVenta'))

    flash('Producto no encontrado en el carrito.', 'warning')
    return redirect(url_for('mostrador.mostradorVenta'))


# ─── ELIMINAR PRODUCTO ──────────────────────────────────────

@mostrador.route("/venta/eliminar/<int:id_producto>", methods=['POST'])
@login_required
@roles_required('Cajero')
def eliminarProducto(id_producto):
    form = EliminarProductoForm()

    if not form.validate_on_submit():
        flash('Acción no válida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    tipo    = request.form.get('tipo', 'producto')
    carrito = _get_carrito_activo()
    nombre  = ''

    for item in carrito:
        match = (
            item.get('id_producto') == id_producto and
            item.get('tipo', 'producto') == tipo
        )
        if match:
            nombre = item['nombre']
            carrito.remove(item)
            break

    _save_carrito_activo(carrito)

    if nombre:
        flash(f'"{nombre}" eliminado del carrito.', 'info')

    return redirect(url_for('mostrador.mostradorVenta'))


# ─── VACIAR CARRITO ─────────────────────────────────────────

@mostrador.route("/venta/vaciar", methods=['POST'])
@login_required
@roles_required('Cajero')
def vaciarCarrito():
    form = VaciarCarritoForm()
    if not form.validate_on_submit():
        flash('Acción no válida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    _save_carrito_activo([])
    flash('Ticket vaciado.', 'info')
    return redirect(url_for('mostrador.mostradorVenta'))


# ─── COBRAR ─────────────────────────────────────────────────

@mostrador.route("/venta/cobrar", methods=['POST'])
@login_required
@roles_required('Cajero')
def cobrar():    
    form = CobrarForm()

    if not form.validate_on_submit():
        flash('Acción no válida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito_items, total = _build_carrito()

    if not carrito_items:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    items_productos = [i for i in carrito_items if i.get('tipo') != 'corte']
    items_cortes    = [i for i in carrito_items if i.get('tipo') == 'corte']

    try:
        # ── 1. Crear el Pedido ────────────────────────────────
        tipo_pago  = form.tipo_pago.data  or 'Efectivo'
        referencia = form.referencia.data or ''

        # Validar que el tipo sea uno de los valores permitidos
        if tipo_pago not in ('Efectivo', 'Tarjeta'):
            tipo_pago = 'Efectivo'

        notas_pago = f'Ref. tarjeta: {referencia}' if tipo_pago == 'Tarjeta' and referencia else None

        pedido = Pedido(
            idUsuario = current_user.id,
            Total     = total,
            Tipo      = tipo_pago,
            Estatus   = 'Finalizado',   # mostrador = venta inmediata
            Entrega   = 'Mostrador',
            Notas     = notas_pago,
        )
        db.session.add(pedido)
        db.session.flush()  # obtener idPedido antes de los detalles

        # ── 2. Procesar productos (unidades) ──────────────────
        for item in items_productos:
            id_producto = item['id_producto']
            cantidad    = int(round(item['cantidad']))

            unidades = (
                ProductoUnitario.query
                .filter_by(idProducto=id_producto, estatus='Disponible')
                .limit(cantidad)
                .all()
            )

            if not unidades:
                raise Exception(
                    f'Sin stock disponible para "{item["nombre"]}".'
                )

            if len(unidades) < cantidad:
                raise Exception(
                    f'Stock insuficiente para "{item["nombre"]}": '
                    f'se pidieron {cantidad} y solo hay {len(unidades)}.'
                )

            for u in unidades:
                u.estatus   = 'Vendido'
                u.idPedido  = pedido.idPedido
                u.idCarrito = None

        # ── 3. Procesar cortes (peso/kg) ──────────────────────
        for item in items_cortes:
            id_corte = item['id_producto']   # reutilizamos la clave del carrito
            peso     = round(float(item['cantidad']), 3)

            # Buscar lote FIFO con stock suficiente
            lote = (
                Lote.query
                .join(CanalCorte, Lote.idCanalCorte == CanalCorte.idCanalCorte)
                .filter(
                    CanalCorte.idCorte == id_corte,
                    Lote.estatus       == 'Disponible',
                    Lote.totalMateria  >= peso,
                )
                .order_by(
                    Lote.fechaCaducidad.is_(None),
                    Lote.fechaCaducidad.asc(),
                    Lote.idLote.asc(),
                )
                .first()
            )

            if not lote:
                raise Exception(
                    f'Sin stock suficiente para el corte "{item["nombre"]}" '
                    f'({peso} kg solicitados).'
                )

            # Descontar del lote
            lote.totalMateria = round(lote.totalMateria - peso, 3)
            if lote.totalMateria <= 0:
                lote.totalMateria = 0.0
                lote.estatus      = 'Agotado'

            # Registrar el CorteUnitario
            corte_u = CorteUnitario(
                idCorte  = id_corte,
                idLote   = lote.idLote,
                idPedido = pedido.idPedido,
                peso     = peso,
                costo    = round(item['precio'] * peso, 2),
                estatus  = 'Vendido',
            )
            db.session.add(corte_u)

        # ── 4. Guardar todo ───────────────────────────────────
        db.session.commit()

        current_app.logger.info(
            f"venta_mostrador | pedido_id={pedido.idPedido} "
            f"| total={total:.2f} | tipo_pago={tipo_pago} "
            f"| productos={len(items_productos)} | cortes={len(items_cortes)} "
            f"| estatus={pedido.Estatus} "
            f"| usuario={current_user.email} "
            f"| ip={request.remote_addr}"
        )

        # ── 5. Limpiar carrito ────────────────────────────────
        _save_carrito_activo([])

        flash(
            f'Venta registrada correctamente. Pedido #MO-{pedido.idPedido:04d}',
            'success'
        )

    except Exception as e:
        db.session.rollback()

        current_app.logger.error(
            f"Error en venta mostrador | usuario={current_user.email} "
            f"| error={str(e)} | total=${total:.2f} "
            f"| ip={request.remote_addr}"
        )
        flash(f'Error al registrar la venta: {str(e)}', 'error')

    return redirect(url_for('mostrador.mostradorVenta'))


# ─── GESTIÓN DE TICKETS ─────────────────────────────────────

@mostrador.route("/venta/ticket/nuevo", methods=['POST'])
@login_required
@roles_required('Cajero')
def nuevoTicket():
    tickets = _get_tickets()
    siguiente = str(max([int(k) for k in tickets.keys()]) + 1)
    tickets[siguiente] = []
    _save_tickets(tickets)
    session['ticket_activo'] = siguiente
    session.modified = True
    return redirect(url_for('mostrador.mostradorVenta'))


@mostrador.route("/venta/ticket/cambiar/<int:num>", methods=['POST'])
@login_required
@roles_required('Cajero')
def cambiarTicket(num):
    tickets = _get_tickets()
    num = str(num)
    if num in tickets:
        session['ticket_activo'] = num
        session.modified = True
    return redirect(url_for('mostrador.mostradorVenta'))


@mostrador.route("/venta/ticket/cerrar/<int:num>", methods=['POST'])
@login_required
@roles_required('Cajero')
def cerrarTicket(num):
    tickets = _get_tickets()
    num = str(num)
    if len(tickets) <= 1:
        flash('No puedes cerrar el único ticket abierto.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    tickets.pop(num, None)
    _save_tickets(tickets)

    if session.get('ticket_activo') == num:
        session['ticket_activo'] = min(tickets.keys(), key=int)
        session.modified = True

    return redirect(url_for('mostrador.mostradorVenta'))


# ─── PEDIDOS — VISTA PRINCIPAL ──────────────────────────────

@mostrador.route("/pedidos", methods=['GET'])
@login_required
@roles_required('Cajero')
def mostradorPedido():
    pedidos = (
        Pedido.query
        .filter(
            Pedido.Entrega == 'Mostrador',
            Pedido.Estatus == 'EnCurso'
        )
        .order_by(Pedido.idPedido.asc())
        .all()
    )

    # Preview por pedido: contar productos y cortes sin cargar todo
    preview_por_pedido = {}
    for p in pedidos:
        n_prod   = p.unidadesPedido.filter_by(estatus='Vendido').count()
        n_cortes = p.cortesPedido.filter_by(estatus='Vendido').count()
        preview_por_pedido[p.idPedido] = {
            'n_prod':   n_prod,
            'n_cortes': n_cortes,
            'total':    n_prod + n_cortes,
        }

    entregar_form = EntregarPedidoForm()

    return render_template(
        "mostrador/pedidos.html",
        pedidos            = pedidos,
        preview_por_pedido = preview_por_pedido,
        entregar_form      = entregar_form,
    )


# ─── PEDIDOS — DETALLE ──────────────────────────────────────

@mostrador.route("/pedidos/detalle/<int:id_pedido>", methods=['GET'])
@login_required
@roles_required('Cajero')
def detallePedido(id_pedido):
    pedido = Pedido.query.filter(
        Pedido.idPedido == id_pedido,
        Pedido.Entrega  == 'Mostrador',
        Pedido.Estatus  == 'EnCurso'
    ).first_or_404()

    # ── Productos ──
    unidades_db = (
        ProductoUnitario.query
        .filter_by(idPedido=id_pedido, estatus='Vendido')
        .all()
    )
    # Agrupar por producto
    productos_agrupados = {}
    for u in unidades_db:
        pid = u.idProducto
        if pid not in productos_agrupados:
            from app.models.producto import Producto as Prod
            prod = Prod.query.get(pid)
            productos_agrupados[pid] = {
                'nombre':   prod.NombreProducto if prod else f'Producto #{pid}',
                'precio':   prod.PrecioVentaProducto if prod else 0.0,
                'cantidad': 0,
                'tipo':     'producto',
            }
        productos_agrupados[pid]['cantidad'] += 1

    items_productos = []
    for d in productos_agrupados.values():
        d['subtotal'] = round(d['precio'] * d['cantidad'], 2)
        items_productos.append(d)

    # ── Cortes ──
    cortes_db = (
        CorteUnitario.query
        .filter_by(idPedido=id_pedido, estatus='Vendido')
        .all()
    )
    items_cortes = [
        {
            'nombre':   cu.corte.nombreCorte if cu.corte else f'Corte #{cu.idCorte}',
            'cantidad': cu.peso,
            'precio':   cu.corte.precioPorKilo if cu.corte else 0.0,
            'subtotal': cu.costo,
            'tipo':     'corte',
        }
        for cu in cortes_db
    ]

    todos = items_productos + items_cortes
    cliente = pedido.user.name if pedido.user else 'Sin cliente'

    return jsonify({
        'idPedido':        pedido.idPedido,
        'cliente':         cliente,
        'total':           pedido.Total,
        'tipo':            pedido.Tipo,
        'estatus':         pedido.Estatus,
        'fecha':           pedido.fechaCreacion.strftime('%d/%m/%Y %H:%M'),
        'num_items':       len(todos),
        'items':           todos,
    })


# ─── PEDIDOS — ENTREGAR ─────────────────────────────────────

@mostrador.route("/pedidos/entregar/<int:id_pedido>", methods=['POST'])
@login_required
@roles_required('Cajero')
def entregarPedido(id_pedido):
    form = EntregarPedidoForm()

    if not form.validate_on_submit():
        flash('Acción no válida.', 'warning')
        return redirect(url_for('mostrador.mostradorPedido'))

    pedido = Pedido.query.filter(
        Pedido.idPedido == id_pedido,
        Pedido.Entrega  == 'Mostrador',
        Pedido.Estatus  == 'EnCurso'
    ).first_or_404()

    try:
        # Si viene tipo_pago del modal de cobro, registrarlo en el pedido
        tipo_pago  = form.tipo_pago.data  or ''
        referencia = form.referencia.data or ''

        if tipo_pago in ('Efectivo', 'Tarjeta'):
            pedido.Tipo = tipo_pago
            if tipo_pago == 'Tarjeta' and referencia:
                notas_actuales = pedido.Notas or ''
                ref_txt = f'Ref. tarjeta: {referencia}'
                pedido.Notas = f'{notas_actuales} | {ref_txt}'.strip(' |') if notas_actuales else ref_txt

        pedido.Estatus = 'Finalizado'
        db.session.commit()

        current_app.logger.info(
            f"pedido_entregado | pedido_id={pedido.idPedido} "
            f"| total={pedido.Total:.2f} | tipo_pago={pedido.Tipo} "
            f"| estatus={pedido.Estatus} "
            f"| usuario={current_user.email} "
            f"| ip={request.remote_addr}"
        )
        
        flash(f'Pedido #{id_pedido:04d} marcado como entregado.', 'success')
    except Exception as e:
        db.session.rollback()
        
        flash(f'Error al actualizar el pedido: {str(e)}', 'error')

    return redirect(url_for('mostrador.mostradorPedido'))