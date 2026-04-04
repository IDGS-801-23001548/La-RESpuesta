from flask import render_template, redirect, url_for, flash, request, jsonify
from . import venta
from app.extensions import db, mongo_fotos
from app.models.producto import Producto
from app.models.producto_unitario import ProductoUnitario
from app.models.carrito import Carrito
from app.models.pedido import Pedido
from app.modules.venta.forms import AgregarAlCarritoForm
from flask_security import login_required
from flask_login import current_user


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _get_or_create_carrito():
    """Devuelve el carrito activo del usuario; lo crea si no existe."""
    carrito = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito:
        carrito = Carrito(idUsuario=current_user.id)
        db.session.add(carrito)
        db.session.commit()
    return carrito


def _carrito_count():
    """Cantidad de unidades en el carrito del usuario actual."""
    carrito = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito:
        return 0
    return carrito.productos.filter_by(estatus='EnCarrito').count()


def _agrupar_unidades(unidades):
    """
    Recibe una lista de ProductoUnitario y devuelve una lista de dicts agrupados
    por producto: [{ producto, cantidad, subtotal, ultima_unidad_id }, ...]
    """
    resumen = {}
    for u in unidades:
        pid = u.idProducto
        if pid not in resumen:
            resumen[pid] = {
                'producto':        u.producto,
                'cantidad':        0,
                'subtotal':        0.0,
                'ultima_unidad_id': u.idProductoUnitario
            }
        resumen[pid]['cantidad'] += 1
        resumen[pid]['subtotal'] += u.producto.PrecioVentaProducto
        resumen[pid]['ultima_unidad_id'] = u.idProductoUnitario
    return list(resumen.values())


def _enrich_productos_con_fotos(productos):
    """
    Recibe una lista de objetos Producto (SQLAlchemy) y devuelve una lista
    de dicts enriquecidos con la foto en base64 obtenida de MongoDB.

    Estructura retornada por elemento:
    {
        'producto': <Producto>,
        'foto_b64': "data:image/jpeg;base64,..." | None
    }
    """
    resultado = []
    for p in productos:
        foto_b64 = None
        if p.idFoto and mongo_fotos is not None:
            try:
                doc = mongo_fotos.find_one({'idFoto': str(p.idFoto)})
                if doc and doc.get('foto'):
                    # La foto ya viene en base64 según la estructura de MongoDB
                    raw = doc['foto']
                    # Si no trae el prefijo data URI, lo agregamos
                    if not raw.startswith('data:'):
                        raw = f'data:image/jpeg;base64,{raw}'
                    foto_b64 = raw
            except Exception:
                pass   # Falla silenciosa: se mostrará el placeholder
        resultado.append({'producto': p, 'foto_b64': foto_b64})
    return resultado


# ─────────────────────────────────────────────
#  INICIO
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
#  CATÁLOGO — SELECCIÓN DE ANIMAL
# ─────────────────────────────────────────────

@venta.route("/seleccionar_animal", methods=['GET'])
@login_required
def seleccionar_animal():
    return render_template(
        "venta/selector_animal.html",
        carrito_count=_carrito_count()
    )


# ─────────────────────────────────────────────
#  CATÁLOGOS POR ANIMAL
# ─────────────────────────────────────────────

def _catalogo_view(categoria, template, emoji, label):
    """
    Helper compartido para los tres catálogos.
    Consulta MySQL filtrando por categoría y stock,
    enriquece con fotos de MongoDB y pasa el form CSRF.
    """
    form = AgregarAlCarritoForm()
    productos_db = Producto.query.filter_by(
        Categoria=categoria
    ).filter(
        Producto.StockProducto > 0
    ).order_by(Producto.NombreProducto).all()

    items = _enrich_productos_con_fotos(productos_db)

    # Precio mínimo y máximo para el slider del frontend
    precios = [p['producto'].PrecioVentaProducto for p in items]
    precio_min = int(min(precios)) if precios else 0
    precio_max = int(max(precios)) if precios else 9999

    return render_template(
        template,
        items=items,
        precio_min=precio_min,
        precio_max=precio_max,
        emoji=emoji,
        label=label,
        form=form,
        carrito_count=_carrito_count()
    )


@venta.route("/catalogo_res", methods=['GET'])
@login_required
def catalogo_res():
    return _catalogo_view('Res', 'venta/catalogo_res.html', '🐄', 'Res')


@venta.route("/catalogo_cerdo", methods=['GET'])
@login_required
def catalogo_cerdo():
    return _catalogo_view('Cerdo', 'venta/catalogo_cerdo.html', '🐷', 'Cerdo')


@venta.route("/catalogo_pollo", methods=['GET'])
@login_required
def catalogo_pollo():
    return _catalogo_view('Pollo', 'venta/catalogo_pollo.html', '🐔', 'Pollo')


# ─────────────────────────────────────────────
#  CARRITO — AGREGAR UNIDAD INDIVIDUAL (por id_producto)
# ─────────────────────────────────────────────

@venta.route("/carrito/agregar/<int:id_producto>", methods=['POST'])
@login_required
def agregar_al_carrito(id_producto):
    """
    Agrega una unidad disponible de un producto concreto al carrito.
    Valida CSRF via AgregarAlCarritoForm.
    Soporta JSON (fetch) y redirect normal.
    """
    form = AgregarAlCarritoForm()
    if not form.validate_on_submit():
        if request.is_json:
            return jsonify({'ok': False, 'msg': 'Token inválido'}), 400
        flash('Solicitud inválida.', 'error')
        return redirect(request.referrer or url_for('venta.seleccionar_animal'))

    producto    = Producto.query.get_or_404(id_producto)
    carrito_obj = _get_or_create_carrito()

    unidad = ProductoUnitario.query.filter_by(
        idProducto=id_producto,
        estatus='Disponible'
    ).first()

    if not unidad:
        if request.is_json:
            return jsonify({'ok': False, 'msg': 'Sin stock disponible'}), 400
        flash('No hay unidades disponibles de ese producto.', 'warning')
        return redirect(request.referrer or url_for('venta.seleccionar_animal'))

    unidad.estatus   = 'EnCarrito'
    unidad.idCarrito = carrito_obj.idCarrito
    db.session.commit()

    if request.is_json:
        return jsonify({
            'ok':            True,
            'carrito_count': _carrito_count(),
            'msg':           f'"{producto.NombreProducto}" agregado al carrito'
        })

    flash(f'"{producto.NombreProducto}" agregado al carrito.', 'success')
    return redirect(request.referrer or url_for('venta.carrito'))


# ─────────────────────────────────────────────
#  CARRITO — QUITAR UNA UNIDAD
# ─────────────────────────────────────────────

@venta.route("/carrito/quitar/<int:id_producto_unitario>", methods=['POST'])
@login_required
def quitar_del_carrito(id_producto_unitario):
    """Devuelve una unidad al stock (estado Disponible)."""
    unidad      = ProductoUnitario.query.get_or_404(id_producto_unitario)
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()

    if not carrito_obj or unidad.idCarrito != carrito_obj.idCarrito:
        if request.is_json:
            return jsonify({'ok': False, 'msg': 'No autorizado'}), 403
        flash('No puedes modificar ese carrito.', 'error')
        return redirect(url_for('venta.carrito'))

    unidad.estatus   = 'Disponible'
    unidad.idCarrito = None
    db.session.commit()

    if request.is_json:
        return jsonify({'ok': True, 'carrito_count': _carrito_count()})

    flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('venta.carrito'))


# ─────────────────────────────────────────────
#  CARRITO — VACIAR TODO
# ─────────────────────────────────────────────

@venta.route("/carrito/vaciar", methods=['POST'])
@login_required
def vaciar_carrito():
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if carrito_obj:
        for u in carrito_obj.productos.filter_by(estatus='EnCarrito').all():
            u.estatus   = 'Disponible'
            u.idCarrito = None
        db.session.commit()

    flash('Carrito vaciado.', 'success')
    return redirect(url_for('venta.seleccionar_animal'))


# ─────────────────────────────────────────────
#  CARRITO — VER
# ─────────────────────────────────────────────

@venta.route("/carrito", methods=['GET'])
@login_required
def carrito():
    carrito_obj = _get_or_create_carrito()
    unidades    = carrito_obj.productos.filter_by(estatus='EnCarrito').all()
    items       = _agrupar_unidades(unidades)
    subtotal    = sum(i['subtotal'] for i in items)
    iva         = round(subtotal * 0.16, 2)
    total       = round(subtotal + iva, 2)

    return render_template(
        "venta/carrito.html",
        items=items,
        subtotal=subtotal,
        iva=iva,
        total=total,
        carrito_count=len(unidades)
    )


# ─────────────────────────────────────────────
#  PAGO — VER
# ─────────────────────────────────────────────

@venta.route("/pago", methods=['GET'])
@login_required
def pago():
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito_obj:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('venta.seleccionar_animal'))

    unidades = carrito_obj.productos.filter_by(estatus='EnCarrito').all()
    if not unidades:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('venta.seleccionar_animal'))

    items    = _agrupar_unidades(unidades)
    subtotal = sum(i['subtotal'] for i in items)
    iva      = round(subtotal * 0.16, 2)
    total    = round(subtotal + iva, 2)

    return render_template(
        "venta/pago.html",
        items=items,
        subtotal=subtotal,
        iva=iva,
        total=total,
        carrito_count=len(unidades)
    )


# ─────────────────────────────────────────────
#  PAGO — CONFIRMAR
# ─────────────────────────────────────────────

@venta.route("/pago/confirmar", methods=['POST'])
@login_required
def confirmar_pago():
    carrito_obj = Carrito.query.filter_by(idUsuario=current_user.id).first()
    if not carrito_obj:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('venta.carrito'))

    unidades = carrito_obj.productos.filter_by(estatus='EnCarrito').all()
    if not unidades:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('venta.carrito'))

    metodo_pago  = request.form.get('metodo_pago', 'Tarjeta')
    tipo_entrega = request.form.get('tipo_entrega', 'Domicilio')
    subtotal     = sum(u.producto.PrecioVentaProducto for u in unidades)
    iva          = round(subtotal * 0.16, 2)
    total        = round(subtotal + iva, 2)

    nuevo_pedido = Pedido(
        idUsuario=current_user.id,
        Total=total,
        Tipo=metodo_pago,
        Estatus='EnCurso',
        Entrega=tipo_entrega
    )
    db.session.add(nuevo_pedido)
    db.session.flush()  # obtiene idPedido antes del commit

    for u in unidades:
        u.estatus   = 'Vendido'
        u.idCarrito = None
        u.idPedido  = nuevo_pedido.idPedido

    db.session.commit()

    flash(f'¡Pedido #VO-{nuevo_pedido.idPedido:04d} confirmado exitosamente!', 'success')
    return redirect(url_for('venta.pedido_detalle', id_pedido=nuevo_pedido.idPedido))


# ─────────────────────────────────────────────
#  PEDIDOS — LISTA
# ─────────────────────────────────────────────

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

    mis_pedidos  = query.order_by(Pedido.idPedido.desc()).all()
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


# ─────────────────────────────────────────────
#  PEDIDOS — DETALLE
# ─────────────────────────────────────────────

@venta.route("/pedido/<int:id_pedido>", methods=['GET'])
@login_required
def pedido_detalle(id_pedido):
    pedido = Pedido.query.filter_by(
        idPedido=id_pedido,
        idUsuario=current_user.id
    ).first_or_404()

    items    = _agrupar_unidades(pedido.unidadesPedido.all())
    subtotal = sum(i['subtotal'] for i in items)
    iva      = round(subtotal * 0.16, 2)

    pasos = {
        'EnCurso':    ['done', 'done', 'active', 'pending'],
        'Finalizado': ['done', 'done', 'done',   'done'],
        'Cancelado':  ['done', 'pending', 'pending', 'pending'],
    }
    timeline = pasos.get(pedido.Estatus, ['done', 'pending', 'pending', 'pending'])

    return render_template(
        "venta/pedido_detalle.html",
        pedido=pedido,
        items=items,
        subtotal=subtotal,
        iva=iva,
        total=pedido.Total,
        timeline=timeline,
        carrito_count=_carrito_count()
    )


# ─────────────────────────────────────────────
#  PEDIDOS — CANCELAR
# ─────────────────────────────────────────────

@venta.route("/pedido/<int:id_pedido>/cancelar", methods=['POST'])
@login_required
def cancelar_pedido(id_pedido):
    pedido = Pedido.query.filter_by(
        idPedido=id_pedido,
        idUsuario=current_user.id
    ).first_or_404()

    if pedido.Estatus != 'EnCurso':
        flash('Solo puedes cancelar pedidos que estén en curso.', 'warning')
        return redirect(url_for('venta.pedido_detalle', id_pedido=id_pedido))

    for u in pedido.unidadesPedido.all():
        u.estatus  = 'Disponible'
        u.idPedido = None

    pedido.Estatus = 'Cancelado'
    db.session.commit()

    flash(f'Pedido #VO-{id_pedido:04d} cancelado. Los productos volvieron al inventario.', 'success')
    return redirect(url_for('venta.pedidos'))


# ─────────────────────────────────────────────
#  AJUSTES — VER
# ─────────────────────────────────────────────

@venta.route("/ajustes", methods=['GET'])
@login_required
def ajustes():
    return render_template(
        "venta/ajustes.html",
        carrito_count=_carrito_count()
    )


# ─────────────────────────────────────────────
#  AJUSTES — GUARDAR DATOS PERSONALES
# ─────────────────────────────────────────────

@venta.route("/ajustes/datos", methods=['POST'])
@login_required
def ajustes_datos():
    nombre    = request.form.get('nombre', '').strip()
    apellido  = request.form.get('apellido', '').strip()
    email     = request.form.get('email', '').strip()
    telefono  = request.form.get('telefono', '').strip()
    direccion = request.form.get('direccion', '').strip()

    if not nombre or not email:
        flash('Nombre y correo son obligatorios.', 'error')
        return redirect(url_for('venta.ajustes'))

    # Email vive en User
    current_user.email = email

    # Datos personales viven en Persona
    persona = current_user.persona
    if not persona:
        # Crear el perfil si por alguna razón no existe
        from app.models.persona import Persona
        persona = Persona(user_id=current_user.id)
        db.session.add(persona)

    persona.nombre           = nombre
    persona.apellido_paterno = apellido
    persona.telefono         = telefono
    persona.direccion        = direccion

    db.session.commit()

    flash('Datos actualizados correctamente.', 'success')
    return redirect(url_for('venta.ajustes'))


# ─────────────────────────────────────────────
#  AJUSTES — CAMBIAR CONTRASEÑA
# ─────────────────────────────────────────────

@venta.route("/ajustes/password", methods=['POST'])
@login_required
def ajustes_password():
    from werkzeug.security import check_password_hash, generate_password_hash

    actual    = request.form.get('password_actual', '')
    nueva     = request.form.get('password_nueva', '')
    confirmar = request.form.get('password_confirmar', '')

    if not check_password_hash(current_user.password, actual):
        flash('La contraseña actual es incorrecta.', 'error')
        return redirect(url_for('venta.ajustes'))

    if len(nueva) < 8:
        flash('La nueva contraseña debe tener al menos 8 caracteres.', 'error')
        return redirect(url_for('venta.ajustes'))

    if nueva != confirmar:
        flash('Las contraseñas nuevas no coinciden.', 'error')
        return redirect(url_for('venta.ajustes'))

    current_user.password = generate_password_hash(nueva)
    db.session.commit()

    flash('Contraseña actualizada correctamente.', 'success')
    return redirect(url_for('venta.ajustes'))
