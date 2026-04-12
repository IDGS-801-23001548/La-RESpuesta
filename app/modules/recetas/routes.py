from flask import render_template, redirect, url_for, flash, request
from . import receta
from .forms import RecetaForm
from app.extensions import db, mongo_fotos
from app.models import (
    Receta, RecetaMateriaPrima,
    Producto, MateriaPrima, MateriaProveida,
    Corte, CanalCorte, Lote, Categoria,
)
from flask_login import login_required
from flask_security import roles_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func


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


def _choices_materias_con_lote():
    """Todas las materias primas disponibles (via MateriaProveida).
    La receta es un plano — no requiere lotes existentes."""
    materias = (
        MateriaProveida.query
        .order_by(MateriaProveida.nombreMateriaProveida)
        .all()
    )
    return [
        {'id': mp.idMateriaProveida, 'nombre': mp.nombreMateriaProveida}
        for mp in materias
    ]


def _choices_cortes_con_lote():
    """Todos los cortes disponibles en el catalogo.
    La receta es un plano — no requiere lotes existentes."""
    cortes = Corte.query.order_by(Corte.nombreCorte).all()
    resultado = []
    for c in cortes:
        cat = c.categoria
        nombre = f"{c.nombreCorte} ({cat.nombreCategoria})" if cat else c.nombreCorte
        resultado.append({'id': c.idCorte, 'nombre': nombre})
    return resultado


def _parse_ingredientes(form_data):
    """Lee del request las listas paralelas de ingredientes materia y corte.

    Campos del form:
      materia_id[]       / materia_cantidad[]
      corte_id[]         / corte_cantidad[]

    Devuelve lista de dicts:
      {'tipo': 'materia', 'id': int, 'cantidad': float}
      {'tipo': 'corte',   'id': int, 'cantidad': float}
    """
    resultado = []

    # Ingredientes tipo materia (idMateriaProveida → lo mapeamos a idMateriaPrima via MateriaProveida)
    mat_ids   = form_data.getlist('materia_id[]')
    mat_cants = form_data.getlist('materia_cantidad[]')
    for raw_id, raw_cant in zip(mat_ids, mat_cants):
        if not raw_id or not raw_cant:
            continue
        try:
            mid  = int(raw_id)
            cant = float(raw_cant)
        except ValueError:
            continue
        if cant <= 0:
            continue
        # Obtener idMateriaPrima desde MateriaProveida
        mp = MateriaProveida.query.get(mid)
        if mp:
            resultado.append({'tipo': 'materia', 'id': mp.idMateriaPrima, 'cantidad': cant})

    # Ingredientes tipo corte (idCorte directo)
    corte_ids   = form_data.getlist('corte_id[]')
    corte_cants = form_data.getlist('corte_cantidad[]')
    for raw_id, raw_cant in zip(corte_ids, corte_cants):
        if not raw_id or not raw_cant:
            continue
        try:
            cid  = int(raw_id)
            cant = float(raw_cant)
        except ValueError:
            continue
        if cant <= 0:
            continue
        resultado.append({'tipo': 'corte', 'id': cid, 'cantidad': cant})

    return resultado


def _guardar_ingredientes(receta_id, ingredientes):
    """Crea los registros RecetaMateriaPrima a partir de la lista de ingredientes parsed."""
    for ing in ingredientes:
        if ing['tipo'] == 'materia':
            db.session.add(RecetaMateriaPrima(
                idReceta       = receta_id,
                idMateriaPrima = ing['id'],
                idCorte        = None,
                cantidadUsada  = ing['cantidad'],
            ))
        else:  # corte
            db.session.add(RecetaMateriaPrima(
                idReceta       = receta_id,
                idMateriaPrima = None,
                idCorte        = ing['id'],
                cantidadUsada  = ing['cantidad'],
            ))


def _ingredientes_actuales(receta_obj):
    """Construye la lista de ingredientes actuales para pre-poblar el form en modo editar.
    Devuelve dos listas: materias y cortes."""
    materias = []
    cortes   = []
    for rm in receta_obj.materiasPrimas.all():
        if rm.idCorte:
            cortes.append({'idCorte': rm.idCorte, 'cantidadUsada': rm.cantidadUsada})
        elif rm.idMateriaPrima:
            # Buscar la MateriaProveida que apunta a esta MateriaPrima
            mp = MateriaProveida.query.filter_by(idMateriaPrima=rm.idMateriaPrima).first()
            materias.append({
                'idMateriaProveida': mp.idMateriaProveida if mp else 0,
                'cantidadUsada': rm.cantidadUsada,
            })
    return materias, cortes


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
        n_materias = r.materiasPrimas.filter(RecetaMateriaPrima.idMateriaPrima.isnot(None)).count()
        n_cortes   = r.materiasPrimas.filter(RecetaMateriaPrima.idCorte.isnot(None)).count()
        items.append({
            'receta':           r,
            'foto_b64':         _foto_b64_de(r.idFoto),
            'num_materias':     n_materias,
            'num_cortes':       n_cortes,
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
    choices_materias = _choices_materias_con_lote()
    choices_cortes   = _choices_cortes_con_lote()

    if form.validate_on_submit():
        producto = Producto.query.get(form.idProducto.data)
        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('receta.recetas_nueva'))

        ingredientes = _parse_ingredientes(request.form)
        if not ingredientes:
            flash('Debes agregar al menos un ingrediente a la receta.', 'danger')
            return render_template(
                'admin/recetas/recetas_form.html',
                form=form, receta=None,
                choices_materias=choices_materias,
                choices_cortes=choices_cortes,
                ingredientes_materias=[], ingredientes_cortes=[],
                foto_actual=None, modo='nuevo',
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
            db.session.flush()
            _guardar_ingredientes(nueva.idReceta, ingredientes)
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
        choices_materias=choices_materias,
        choices_cortes=choices_cortes,
        ingredientes_materias=[],
        ingredientes_cortes=[],
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
    choices_materias = _choices_materias_con_lote()
    choices_cortes   = _choices_cortes_con_lote()

    if form.validate_on_submit():
        producto = Producto.query.get(form.idProducto.data)
        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('receta.recetas_editar', id=id))

        ingredientes = _parse_ingredientes(request.form)
        if not ingredientes:
            flash('Debes agregar al menos un ingrediente a la receta.', 'danger')
        else:
            receta_obj.idProducto   = producto.idProducto
            receta_obj.nombreReceta = producto.NombreProducto
            receta_obj.idFoto       = producto.idFoto
            receta_obj.descripcion  = form.descripcion.data.strip() if form.descripcion.data else None

            # Reemplazar ingredientes
            RecetaMateriaPrima.query.filter_by(idReceta=receta_obj.idReceta).delete()
            _guardar_ingredientes(receta_obj.idReceta, ingredientes)
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

    ing_materias, ing_cortes = _ingredientes_actuales(receta_obj)

    return render_template(
        'admin/recetas/recetas_form.html',
        form=form,
        receta=receta_obj,
        choices_materias=choices_materias,
        choices_cortes=choices_cortes,
        ingredientes_materias=ing_materias,
        ingredientes_cortes=ing_cortes,
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
