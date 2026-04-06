from flask import render_template, redirect, url_for, flash, request
from . import materia
from .forms import MateriaPrimaForm
from app.extensions import db
from app.models.materia_prima import MateriaPrima
from flask_login import login_required
from flask_security import roles_required


@materia.route('/materia-prima')
@login_required
@roles_required('admin')
def materias():
    todas = MateriaPrima.query.order_by(MateriaPrima.nombre).all()
    return render_template('admin/materia/materia.html', materias=todas)


@materia.route('/materia-prima/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def materia_nueva():
    form = MateriaPrimaForm()
    if form.validate_on_submit():
        es_reventa = form.categoria.data == 'Reventa'
        nueva = MateriaPrima(
            nombre            = form.nombre.data.strip(),
            descripcion       = form.descripcion.data.strip() or None,
            categoria         = form.categoria.data,
            unidad_compra     = form.unidad_compra.data,
            unidad_estandar   = form.unidad_estandar.data,
            # Reventa no tiene conversión ni merma
            factor_conversion = None if es_reventa else form.factor_conversion.data,
            tipo_merma        = None if es_reventa else (_csv(form.tipo_merma.data) or None),
            pct_merma         = 0    if es_reventa else (form.pct_merma.data or 0),
            stock_minimo      = form.stock_minimo.data or 0,
            costo_promedio    = form.costo_promedio.data or 0,
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Materia prima registrada correctamente.', 'success')
        return redirect(url_for('materia.materias'))
    return render_template('admin/materia/materia_form.html', materia=None, form=form)


@materia.route('/materia-prima/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def materia_editar(id):
    mat = MateriaPrima.query.get_or_404(id)
    form = MateriaPrimaForm(obj=mat)

    if request.method == 'GET':
        # SelectMultipleField necesita lista; el modelo almacena CSV
        form.tipo_merma.data = mat.tipo_merma_lista

    if form.validate_on_submit():
        es_reventa = form.categoria.data == 'Reventa'
        mat.nombre            = form.nombre.data.strip()
        mat.descripcion       = form.descripcion.data.strip() or None
        mat.categoria         = form.categoria.data
        mat.unidad_compra     = form.unidad_compra.data
        mat.unidad_estandar   = form.unidad_estandar.data
        mat.factor_conversion = None if es_reventa else form.factor_conversion.data
        mat.tipo_merma        = None if es_reventa else (_csv(form.tipo_merma.data) or None)
        mat.pct_merma         = 0    if es_reventa else (form.pct_merma.data or 0)
        mat.stock_minimo      = form.stock_minimo.data or 0
        mat.costo_promedio    = form.costo_promedio.data or 0
        db.session.commit()
        flash('Materia prima actualizada correctamente.', 'success')
        return redirect(url_for('materia.materias'))

    return render_template('admin/materia/materia_form.html', materia=mat, form=form)


@materia.route('/materia-prima/<int:id>/eliminar', methods=['POST'])
@login_required
@roles_required('admin')
def materia_eliminar(id):
    mat = MateriaPrima.query.get_or_404(id)
    db.session.delete(mat)
    db.session.commit()
    flash('Materia prima eliminada.', 'info')
    return redirect(url_for('materia.materias'))


# ── Stub para la alerta de stock bajo en materia.html ─────────────────────────
@materia.route('/materia-prima/compras/nueva')
@login_required
@roles_required('admin')
def compras_nueva():
    # Pendiente: módulo de compras
    flash('El módulo de compras aún no está disponible.', 'info')
    return redirect(url_for('materia.materias'))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _csv(lista):
    """Convierte una lista de strings a CSV.  Retorna '' si está vacía."""
    return ','.join(lista) if lista else ''
