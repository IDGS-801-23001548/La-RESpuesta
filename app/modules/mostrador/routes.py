from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from flask_security.decorators import roles_required
from . import mostrador
from datetime import datetime
import uuid
from app.extensions import db, mongo_fotos
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.ticket import Ticket
from app.models.vistaResumenPedido import VistaResumenPedido
from app.models.detallesTicket import DetalleTicket
from .forms import (
    AgregarProductoForm,
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


def _enrich_productos_con_fotos(productos):
    """
    Recibe una lista de objetos Producto (SQLAlchemy) y devuelve una lista
    de dicts enriquecidos con la foto en base64 obtenida de MongoDB.
    """
    resultado = []
    for p in productos:
        foto_b64 = None
        if p.idFoto and mongo_fotos is not None:
            try:
                doc = mongo_fotos.find_one({'idFoto': str(p.idFoto)})
                if doc and doc.get('foto'):
                    raw = doc['foto']
                    if not raw.startswith('data:'):
                        raw = f'data:image/jpeg;base64,{raw}'
                    foto_b64 = raw
            except Exception:
                pass
        resultado.append({'producto': p, 'foto_b64': foto_b64})
    return resultado    

@mostrador.route("/venta", methods=['GET'])
@login_required
@roles_required('Cajero')
def mostradorVenta():
    if 'tickets' not in session:
        session['tickets'] = {'1': []}
        session['ticket_activo'] = '1'
        session.modified = True
    else:
        # Limpiar sesiones viejas con claves mixtas
        session['tickets'] = {str(k): v for k, v in session['tickets'].items()}
        session['ticket_activo'] = str(session.get('ticket_activo', '1'))
        session.modified = True


    productos      = Producto.query.order_by(Producto.NombreProducto).all()
    carrito_items, total = _build_carrito()
    tickets        = _get_tickets()
    ticket_activo  = _get_ticket_activo()

    agregar_form   = AgregarProductoForm()
    modificar_form = ModificarCantidadForm()
    eliminar_form  = EliminarProductoForm()
    vaciar_form    = VaciarCarritoForm()
    cobrar_form    = CobrarForm()
    items          = _enrich_productos_con_fotos(productos)

    return render_template(
        "mostrador/mostrador.html",
        productos      = productos,
        carrito        = carrito_items,
        total          = total,
        items          = items,
        tickets        = tickets,
        ticket_activo  = ticket_activo,
        agregar_form   = agregar_form,
        modificar_form = modificar_form,
        eliminar_form  = eliminar_form,
        vaciar_form    = vaciar_form,
        cobrar_form    = cobrar_form,
    )


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
        if item['id_producto'] == id_producto:
            nueva_cantidad = round(item['cantidad'] + cantidad, 3)
            if nueva_cantidad > producto.StockProducto:
                flash(
                    f'Stock insuficiente. Máximo disponible: '
                    f'{producto.StockProducto} {item["unidad"]}.',
                    'warning'
                )
                return redirect(url_for('mostrador.mostradorVenta'))
            item['cantidad'] = nueva_cantidad
            _save_carrito_activo(carrito)
            flash(f'"{producto.NombreProducto}" actualizado en el carrito.', 'success')
            return redirect(url_for('mostrador.mostradorVenta'))

    

    if cantidad > producto.StockProducto:
        flash(
            f'Stock insuficiente. Máximo disponible: '
            f'{producto.StockProducto}.',
            'warning'
        )
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito.append({
        'id_producto': id_producto,
        'nombre':      producto.NombreProducto,
        'precio':      producto.PrecioVentaProducto,
        'cantidad':    round(cantidad, 3),
        'stock':       producto.StockProducto,
    })

    _save_carrito_activo(carrito)
    flash(f'"{producto.NombreProducto}" agregado al carrito.', 'success')
    return redirect(url_for('mostrador.mostradorVenta'))


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
    carrito  = _get_carrito_activo()

    for item in carrito:
        if item['id_producto'] == id_producto:
            if accion == 'sumar':
                nueva_cantidad = cantidad + 1
            elif accion == 'restar':
                nueva_cantidad = cantidad - 1
            else:
                nueva_cantidad = cantidad

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


@mostrador.route("/venta/eliminar/<int:id_producto>", methods=['POST'])
@login_required
@roles_required('Cajero')
def eliminarProducto(id_producto):
    form = EliminarProductoForm()

    if not form.validate_on_submit():
        flash('Acción no válida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito = _get_carrito_activo()
    nombre  = ''

    for item in carrito:
        if item['id_producto'] == id_producto:
            nombre = item['nombre']
            carrito.remove(item)
            break

    _save_carrito_activo(carrito)

    if nombre:
        flash(f'"{nombre}" eliminado del carrito.', 'info')

    return redirect(url_for('mostrador.mostradorVenta'))


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

    try:
        # ── 1. Generar el ticket ──────────────────────────────
        folio = f"TK-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        ticket = Ticket(
            folioTicket = folio,
            fechaCompra = datetime.now(),
            totalCompra = total,
        )
        db.session.add(ticket)
        db.session.flush()

        for item in carrito_items:
            detalle = DetalleTicket(
                idTicket   = ticket.idTicket,
                idProducto = item['id_producto'],
                cantidad   = item['cantidad'],
                subtotal   = item['subtotal'],
            )
            db.session.add(detalle)

        db.session.commit()

        # ── 2. Crear el pedido via procedure ──────────────────
        conn = db.engine.raw_connection()
        try:
            cursor = conn.cursor()

            # Procedure 1: crear pedido
            cursor.execute('CALL crear_pedido_mostrador(%s, %s)', (current_user.id, 'Efectivo'))
            row = cursor.fetchone()

            if not row:
                raise Exception('El procedure no devolvió un idPedido válido.')

            id_pedido = row[0]

            # Procedure 2: asignar cada producto al pedido
            for item in carrito_items:
                cursor.nextset()  # limpiar resultset anterior antes del siguiente CALL
                cursor.execute('CALL asignar_productos_a_pedido(%s, %s, %s)', (
                    id_pedido,
                    item['id_producto'],
                    item['cantidad'],
                ))

            conn.commit()

        finally:
            cursor.close()
            conn.close()
        
        # ── 3. Limpiar carrito ────────────────────────────────
        _save_carrito_activo([])

        flash(f'Venta registrada correctamente. Folio: {folio}', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar la venta: {str(e)}', 'error')

    return redirect(url_for('mostrador.mostradorVenta'))

# ─── GESTIÓN DE TICKETS ─────────────────────────────────────

@mostrador.route("/venta/ticket/nuevo", methods=['POST'])
@login_required
@roles_required('Cajero')
def nuevoTicket():
    tickets = _get_tickets()
    # El siguiente número es el máximo actual + 1
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
    # No permitir cerrar si es el único ticket
    if len(tickets) <= 1:
        flash('No puedes cerrar el único ticket abierto.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    tickets.pop(num, None)
    _save_tickets(tickets)

    # Si se cerró el activo, cambiar al primero disponible
    if session.get('ticket_activo') == num:
        session['ticket_activo'] = min(tickets.keys(), key=int)
        session.modified = True

    return redirect(url_for('mostrador.mostradorVenta'))

# ─────────────────────────────────────────────────────────────
#  PEDIDOS — VISTA PRINCIPAL
# ─────────────────────────────────────────────────────────────
@mostrador.route("/pedidos", methods=['GET'])
@login_required
@roles_required('Cajero')
def mostradorPedido():
    # Solo pedidos de tipo Mostrador que no estén finalizados ni cancelados
    pedidos = (
        Pedido.query
        .filter(
            Pedido.Entrega == 'Mostrador',
            Pedido.Estatus == 'EnCurso'
        )
        .order_by(Pedido.idPedido.asc())
        .all()
    )

     # Cargar resumen de productos por pedido desde la vista
    ids_pedidos = [p.idPedido for p in pedidos]
    renglones = (
        VistaResumenPedido.query
        .filter(VistaResumenPedido.idPedido.in_(ids_pedidos))
        .all()
    )

    # Agrupar por idPedido → dict { idPedido: [renglones] }
    resumen_por_pedido = {}
    for r in renglones:
        resumen_por_pedido.setdefault(r.idPedido, []).append(r)

    entregar_form = EntregarPedidoForm()

    return render_template(
        "mostrador/pedidos.html",
        pedidos       = pedidos,
        resumen_por_pedido = resumen_por_pedido,
        entregar_form = entregar_form,
    )


# ─────────────────────────────────────────────────────────────
#  PEDIDOS — DETALLE (JSON para el panel derecho)
# ─────────────────────────────────────────────────────────────
@mostrador.route("/pedidos/detalle/<int:id_pedido>", methods=['GET'])
@login_required
@roles_required('Cajero')
def detallePedido(id_pedido):
    pedido = Pedido.query.filter(
        Pedido.idPedido == id_pedido,
        Pedido.Entrega  == 'Mostrador',
        Pedido.Estatus  == 'EnCurso'
    ).first_or_404()

    cliente = pedido.user.name if pedido.user else 'Cliente desconocido'

    renglones = (
        VistaResumenPedido.query
        .filter(VistaResumenPedido.idPedido == id_pedido)
        .all()
    )

    unidades = [
        {
            'nombre':   r.NombreProducto,
            'cantidad': r.cantidad,
            'precio':   r.PrecioVentaProducto,
            'subtotal': r.subtotal,
        }
        for r in renglones
    ]

    return jsonify({
        'idPedido':      pedido.idPedido,
        'cliente':       cliente,
        'total':         pedido.Total,
        'tipo':          pedido.Tipo,
        'estatus':       pedido.Estatus,
        'num_productos': len(unidades),   # ← conteo real desde la vista
        'unidades':      unidades,
    })


# ─────────────────────────────────────────────────────────────
#  PEDIDOS — ENTREGAR
# ─────────────────────────────────────────────────────────────
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
        pedido.Estatus = 'Finalizado'
        db.session.commit()
        flash(f'Pedido #{id_pedido:04d} marcado como entregado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el pedido: {str(e)}', 'error')

    return redirect(url_for('mostrador.mostradorPedido'))