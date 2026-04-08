from flask import render_template, redirect, url_for, flash, request
from . import receta
from .forms import RecetaForm
from app.extensions import db, mongo_fotos
from app.models import (
    Receta, RecetaMateriaPrima,
    Producto, MateriaPrima,
)
from flask_login import login_required
from flask_security import roles_required
from sqlalchemy.exc import IntegrityError


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _foto_b64_de(id_foto):
    """Devuelve la foto en base64 desde MongoDB para mostrarla en templates."""
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


def _choices_productos_disponibles(receta_actual=None):
    """Productos que aun no tienen receta vinculada (excepto el actual si estamos editando)."""
    productos_con_receta_q = db.session.query(Receta.idProducto)
    if receta_actual is not None:
        productos_con_receta_q = productos_con_receta_q.filter(Receta.idReceta != receta_actual.idReceta)
    ids_excluir = {row[0] for row in productos_con_receta_q.all()}

    productos = (
        Producto.query
        .filter(~Producto.idProducto.in_(ids_excluir) if ids_excluir else True)
        .order_by(Producto.NombreProducto)
        .all()
    )
    return [(p.idProducto, p.NombreProducto) for p in productos]


def _parse_ingredientes(form_data):
    """Lee del request las listas paralelas ingrediente_id[] y ingrediente_cantidad[],
    devuelve lista de tuplas (idMateriaPrima:int, cantidad:float). Filtra filas vacias."""
    ids        = form_data.getlist('ingrediente_id[]')
    cantidades = form_data.getlist('ingrediente_cantidad[]')
    resultado  = []
    for raw_id, raw_cant in zip(ids, cantidades):
        if not raw_id or not raw_cant:
            continue
        try:
            mid  = int(raw_id)
            cant = float(raw_cant)
        except ValueError:
            continue
        if cant <= 0:
            continue
        resultado.append((mid, cant))
    return resultado


# ─────────────────────────────────────────────
#  LISTADO
# ─────────────────────────────────────────────

@receta.route('/recetas')
@login_required
@roles_required('admin')
def recetas():
    todas = Receta.query.order_by(Receta.nombreReceta).all()

    items = []
    for r in todas:
        items.append({
            'receta':           r,
            'foto_b64':         _foto_b64_de(r.idFoto),
            'num_materias':     r.materiasPrimas.count(),
            'producto_nombre':  r.producto.NombreProducto if r.producto else '—',
        })

    return render_template(
        'admin/recetas/recetas.html',
        items=items,
        total=len(items),
    )


# ─────────────────────────────────────────────
#  NUEVA
# ─────────────────────────────────────────────

@receta.route('/recetas/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def recetas_nueva():
    form = RecetaForm()
    form.idProducto.choices = _choices_productos_disponibles()
    materias = MateriaPrima.query.order_by(MateriaPrima.nombreMateriaPrima).all()

    if form.validate_on_submit():
        producto = Producto.query.get(form.idProducto.data)
        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('receta.recetas_nueva'))

        ingredientes = _parse_ingredientes(request.form)
        if not ingredientes:
            flash('Debes agregar al menos una materia prima a la receta.', 'danger')
            return render_template(
                'admin/recetas/recetas_form.html',
                form=form, receta=None, materias=materias,
                ingredientes_actuales=[], foto_actual=None, modo='nuevo',
            )

        nueva = Receta(
            nombreReceta = producto.NombreProducto,
            idProducto   = producto.idProducto,
            idFoto       = producto.idFoto,
            descripcion  = form.descripcion.data.strip() if form.descripcion.data else None,
            tipo         = 'MateriaPrima',
        )
        db.session.add(nueva)
        try:
            db.session.flush()  # obtener idReceta
            for mid, cant in ingredientes:
                db.session.add(RecetaMateriaPrima(
                    idReceta       = nueva.idReceta,
                    idMateriaPrima = mid,
                    cantidadUsada  = cant,
                ))
            db.session.commit()
            flash(f'Receta "{nueva.nombreReceta}" creada correctamente.', 'success')
            return redirect(url_for('receta.recetas'))
        except IntegrityError:
            db.session.rollback()
            flash(f'Ya existe una receta para el producto "{producto.NombreProducto}".', 'danger')

    return render_template(
        'admin/recetas/recetas_form.html',
        form=form,
        receta=None,
        materias=materias,
        ingredientes_actuales=[],
        foto_actual=None,
        modo='nuevo',
    )


# ─────────────────────────────────────────────
#  EDITAR
# ─────────────────────────────────────────────

@receta.route('/recetas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def recetas_editar(id):
    receta_obj = Receta.query.get_or_404(id)
    form       = RecetaForm()
    form.idProducto.choices = _choices_productos_disponibles(receta_actual=receta_obj)
    materias   = MateriaPrima.query.order_by(MateriaPrima.nombreMateriaPrima).all()

    if form.validate_on_submit():
        producto = Producto.query.get(form.idProducto.data)
        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('receta.recetas_editar', id=id))

        ingredientes = _parse_ingredientes(request.form)
        if not ingredientes:
            flash('Debes agregar al menos una materia prima a la receta.', 'danger')
        else:
            receta_obj.idProducto   = producto.idProducto
            receta_obj.nombreReceta = producto.NombreProducto
            receta_obj.idFoto       = producto.idFoto
            receta_obj.descripcion  = form.descripcion.data.strip() if form.descripcion.data else None

            # Reemplazar ingredientes (delete-orphan via cascade)
            RecetaMateriaPrima.query.filter_by(idReceta=receta_obj.idReceta).delete()
            for mid, cant in ingredientes:
                db.session.add(RecetaMateriaPrima(
                    idReceta       = receta_obj.idReceta,
                    idMateriaPrima = mid,
                    cantidadUsada  = cant,
                ))
            try:
                db.session.commit()
                flash('Receta actualizada correctamente.', 'success')
                return redirect(url_for('receta.recetas'))
            except IntegrityError:
                db.session.rollback()
                flash('No se pudo actualizar la receta.', 'danger')

    if request.method == 'GET':
        form.idProducto.data = receta_obj.idProducto
        form.descripcion.data = receta_obj.descripcion or ''

    ingredientes_actuales = [
        {'idMateriaPrima': rm.idMateriaPrima, 'cantidadUsada': rm.cantidadUsada}
        for rm in receta_obj.materiasPrimas.all()
    ]

    return render_template(
        'admin/recetas/recetas_form.html',
        form=form,
        receta=receta_obj,
        materias=materias,
        ingredientes_actuales=ingredientes_actuales,
        foto_actual=_foto_b64_de(receta_obj.idFoto),
        modo='editar',
    )


# ─────────────────────────────────────────────
#  ELIMINAR
# ─────────────────────────────────────────────

@receta.route('/recetas/<int:id>/eliminar', methods=['POST'])
@login_required
@roles_required('admin')
def recetas_eliminar(id):
    receta_obj = Receta.query.get_or_404(id)
    nombre     = receta_obj.nombreReceta
    try:
        db.session.delete(receta_obj)
        db.session.commit()
        flash(f'Receta "{nombre}" eliminada.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar la receta porque tiene solicitudes asociadas.', 'danger')
    return redirect(url_for('receta.recetas'))
