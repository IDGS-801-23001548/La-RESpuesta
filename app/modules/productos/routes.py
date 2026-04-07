import base64
from flask import render_template, redirect, url_for, flash, request
from . import productos
from .forms import ProductoForm, ProductoNuevoForm
from app.extensions import db, mongo_fotos
from app.models.producto import Producto
from app.models.categoria import Categoria
from flask_login import login_required
from flask_security import roles_required


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

ANIMALES = ['Res', 'Cerdo', 'Pollo', 'Borrego']

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


def _enrich_productos_con_fotos(productos_list):
    """Enriquece una lista de Producto con la foto base64 de MongoDB."""
    resultado = []
    for p in productos_list:
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


def _next_id_foto():
    """Devuelve el siguiente idFoto (str) disponible en MongoDB."""
    if mongo_fotos is None:
        return None
    docs = list(mongo_fotos.find({}, {'idFoto': 1, '_id': 0}))
    ids = []
    for d in docs:
        try:
            ids.append(int(d['idFoto']))
        except (ValueError, KeyError):
            pass
    return str(max(ids) + 1) if ids else '1'


def _guardar_foto(archivo):
    """Lee un FileStorage, lo convierte a base64 y lo inserta en MongoDB.
    Devuelve el idFoto (str) asignado, o None si no hay MongoDB."""
    if not archivo or not archivo.filename:
        return None
    if mongo_fotos is None:
        return None

    raw_bytes = archivo.read()
    b64 = base64.b64encode(raw_bytes).decode('utf-8')

    fname = archivo.filename.lower()
    if fname.endswith('.png'):
        mime = 'image/png'
    elif fname.endswith('.webp'):
        mime = 'image/webp'
    else:
        mime = 'image/jpeg'

    b64_full = f'data:{mime};base64,{b64}'
    id_foto  = _next_id_foto()
    mongo_fotos.insert_one({'idFoto': id_foto, 'foto': b64_full})
    return id_foto


def _actualizar_foto(id_foto_actual, archivo):
    """Reemplaza la foto en MongoDB si se sube un archivo nuevo.
    Si el producto no tenía foto, crea un registro nuevo.
    Devuelve el idFoto (str) resultante."""
    if not archivo or not archivo.filename:
        return id_foto_actual  # sin cambios

    if mongo_fotos is None:
        return id_foto_actual

    raw_bytes = archivo.read()
    b64 = base64.b64encode(raw_bytes).decode('utf-8')

    fname = archivo.filename.lower()
    if fname.endswith('.png'):
        mime = 'image/png'
    elif fname.endswith('.webp'):
        mime = 'image/webp'
    else:
        mime = 'image/jpeg'

    b64_full = f'data:{mime};base64,{b64}'

    if id_foto_actual:
        mongo_fotos.update_one(
            {'idFoto': str(id_foto_actual)},
            {'$set': {'foto': b64_full}}
        )
        return id_foto_actual
    else:
        id_foto = _next_id_foto()
        mongo_fotos.insert_one({'idFoto': id_foto, 'foto': b64_full})
        return id_foto


def _get_foto_actual(id_foto):
    """Recupera la foto base64 actual de MongoDB dado un idFoto."""
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


def _choices_categorias():
    return [(0, '— Sin categoría —')] + [
        (c.idCategoria, c.nombreCategoria)
        for c in Categoria.query.order_by(Categoria.nombreCategoria).all()
    ]


# ─────────────────────────────────────────────
#  CATÁLOGO ADMINISTRATIVO
# ─────────────────────────────────────────────

@productos.route('/productos')
@login_required
@roles_required('admin')
def catalogo():
    todos_los_productos = (
        Producto.query
        .join(Categoria, Producto.idCategoria == Categoria.idCategoria, isouter=True)
        .order_by(Producto.NombreProducto)
        .all()
    )

    items = _enrich_productos_con_fotos(todos_los_productos)

    precios    = [i['producto'].PrecioVentaProducto for i in items]
    precio_min = int(min(precios)) if precios else 0
    precio_max = int(max(precios)) if precios else 9999

    total_productos = len(items)
    sin_stock       = sum(1 for i in items if i['producto'].StockProducto == 0)
    con_foto        = sum(1 for i in items if i['foto_b64'])

    return render_template(
        'admin/productos/catalogo_productos.html',
        items=items,
        precio_min=precio_min,
        precio_max=precio_max,
        total_productos=total_productos,
        sin_stock=sin_stock,
        con_foto=con_foto,
        animales=ANIMALES,
        emoji_map=EMOJI_MAP,
        color_map=COLOR_MAP,
    )


# ─────────────────────────────────────────────
#  NUEVO PRODUCTO
# ─────────────────────────────────────────────

@productos.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def productos_nuevo():
    form = ProductoNuevoForm()
    form.idCategoria.choices = _choices_categorias()

    if form.validate_on_submit():
        id_categoria = form.idCategoria.data if form.idCategoria.data != 0 else None
        id_foto      = _guardar_foto(form.foto.data)

        nuevo = Producto(
            NombreProducto       = form.NombreProducto.data.strip(),
            DescripcionProducto  = form.DescripcionProducto.data.strip() or None,
            PrecioCompraProducto = form.PrecioCompraProducto.data,
            PrecioVentaProducto  = form.PrecioVentaProducto.data,
            StockProducto        = 0,
            idCategoria          = id_categoria,
            idFoto               = id_foto,
        )
        db.session.add(nuevo)
        db.session.commit()
        flash(f'Producto "{nuevo.NombreProducto}" creado correctamente.', 'success')
        return redirect(url_for('productos.catalogo'))

    return render_template(
        'admin/productos/productos_form.html',
        form=form,
        modo='nuevo',
        producto=None,
        foto_actual=None,
        emoji_map=EMOJI_MAP,
    )


# ─────────────────────────────────────────────
#  EDITAR PRODUCTO
# ─────────────────────────────────────────────

@productos.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def productos_editar(id):
    producto = Producto.query.get_or_404(id)
    form     = ProductoForm(obj=producto)
    form.idCategoria.choices = _choices_categorias()

    foto_actual = _get_foto_actual(producto.idFoto)

    if form.validate_on_submit():
        id_categoria    = form.idCategoria.data if form.idCategoria.data != 0 else None
        nuevo_id_foto   = _actualizar_foto(producto.idFoto, form.foto.data)

        producto.NombreProducto       = form.NombreProducto.data.strip()
        producto.DescripcionProducto  = form.DescripcionProducto.data.strip() or None
        producto.PrecioCompraProducto = form.PrecioCompraProducto.data
        producto.PrecioVentaProducto  = form.PrecioVentaProducto.data
        producto.idCategoria          = id_categoria
        producto.idFoto               = nuevo_id_foto

        db.session.commit()
        flash(f'Producto "{producto.NombreProducto}" actualizado correctamente.', 'success')
        return redirect(url_for('productos.catalogo'))

    if request.method == 'GET':
        form.idCategoria.data = producto.idCategoria or 0

    return render_template(
        'admin/productos/productos_form.html',
        form=form,
        modo='editar',
        producto=producto,
        foto_actual=foto_actual,
        emoji_map=EMOJI_MAP,
    )
