from flask import render_template, redirect, url_for, flash, request, session
from . import mostrador
from app.extensions import db
from app.models.producto import Producto
from .forms import (
    AgregarProductoForm,
    ModificarCantidadForm,
    EliminarProductoForm,
    VaciarCarritoForm,
)


def _calcular_subtotal(item):
    return round(item['precio'] * item['cantidad'], 2)


def _build_carrito():
    carrito_raw = session.get('carrito', [])
    carrito_items = []
    total = 0.0
    for item in carrito_raw:
        subtotal = _calcular_subtotal(item)
        total += subtotal
        carrito_items.append({**item, 'subtotal': subtotal})
    return carrito_items, round(total, 2)


@mostrador.route("/venta", methods=['GET'])
def mostradorVenta():
    if 'carrito' not in session:
        session['carrito'] = []

    productos = Producto.query.order_by(Producto.NombreProducto).all()
    carrito_items, total = _build_carrito()

    agregar_form    = AgregarProductoForm()
    modificar_form  = ModificarCantidadForm()
    eliminar_form   = EliminarProductoForm()
    vaciar_form     = VaciarCarritoForm()

    return render_template(
        "mostrador/mostrador.html",
        productos      = productos,
        carrito        = carrito_items,
        total          = total,
        agregar_form   = agregar_form,
        modificar_form = modificar_form,
        eliminar_form  = eliminar_form,
        vaciar_form    = vaciar_form,
    )


@mostrador.route("/venta/agregar/<int:id_producto>", methods=['POST'])
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

    carrito = session.get('carrito', [])

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
            session['carrito'] = carrito
            session.modified = True
            flash(f'"{producto.NombreProducto}" actualizado en el carrito.', 'success')
            return redirect(url_for('mostrador.mostradorVenta'))

    primera_unidad = producto.unidades.first()
    nombre_unidad  = primera_unidad.NombreUnidad if primera_unidad else 'kg'

    if cantidad > producto.StockProducto:
        flash(
            f'Stock insuficiente. Máximo disponible: '
            f'{producto.StockProducto} {nombre_unidad}.',
            'warning'
        )
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito.append({
        'id_producto': id_producto,
        'nombre':      producto.NombreProducto,
        'precio':      producto.PrecioVentaProducto,
        'unidad':      nombre_unidad,
        'cantidad':    round(cantidad, 3),
        'stock':       producto.StockProducto,
    })

    session['carrito'] = carrito
    session.modified = True
    flash(f'"{producto.NombreProducto}" agregado al carrito.', 'success')
    return redirect(url_for('mostrador.mostradorVenta'))


@mostrador.route("/venta/modificar/<int:id_producto>", methods=['POST'])
def modificarCantidad(id_producto):
    form = ModificarCantidadForm()

    if not form.validate_on_submit():
        flash('Cantidad inválida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    cantidad = form.cantidad.data
    accion   = request.form.get('accion')   # 'sumar' | 'restar' | None
    carrito  = session.get('carrito', [])

    for item in carrito:
        if item['id_producto'] == id_producto:
            if accion == 'sumar':
                nueva_cantidad = cantidad + 0.1
            elif accion == 'restar':
                nueva_cantidad = cantidad - 0.1
            else:
                nueva_cantidad = cantidad

            if nueva_cantidad <= 0:
                carrito.remove(item)
                session['carrito'] = carrito
                session.modified = True
                flash(f'"{item["nombre"]}" eliminado del carrito.', 'info')
                return redirect(url_for('mostrador.mostradorVenta'))

            if nueva_cantidad > item['stock']:
                flash(
                    f'Stock insuficiente. Máximo: {item["stock"]} {item["unidad"]}.',
                    'warning'
                )
                return redirect(url_for('mostrador.mostradorVenta'))

            item['cantidad'] = round(nueva_cantidad, 3)
            session['carrito'] = carrito
            session.modified = True
            return redirect(url_for('mostrador.mostradorVenta'))

    flash('Producto no encontrado en el carrito.', 'warning')
    return redirect(url_for('mostrador.mostradorVenta'))


@mostrador.route("/venta/eliminar/<int:id_producto>", methods=['POST'])
def eliminarProducto(id_producto):
    form = EliminarProductoForm()

    if not form.validate_on_submit():
        flash('Acción no válida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    carrito = session.get('carrito', [])
    nombre  = ''

    for item in carrito:
        if item['id_producto'] == id_producto:
            nombre = item['nombre']
            carrito.remove(item)
            break

    session['carrito'] = carrito
    session.modified = True

    if nombre:
        flash(f'"{nombre}" eliminado del carrito.', 'info')

    return redirect(url_for('mostrador.mostradorVenta'))


@mostrador.route("/venta/vaciar", methods=['POST'])
def vaciarCarrito():
    form = VaciarCarritoForm()

    if not form.validate_on_submit():
        flash('Acción no válida.', 'warning')
        return redirect(url_for('mostrador.mostradorVenta'))

    session.pop('carrito', None)
    session.modified = True
    flash('Carrito vaciado.', 'info')
    return redirect(url_for('mostrador.mostradorVenta'))


@mostrador.route("/pedidos", methods=['GET'])
def mostradorPedido():
    return render_template("mostrador/pedido.html")