from flask import render_template, redirect, url_for, flash, request
from . import materia
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.models.materia_prima import MateriaPrima
from app.models.materia_proveida import MateriaProveida
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.proveedor import Proveedor
from app.models.unidad_medida import UnidadMedida
from flask_login import login_required
from flask_security import roles_required


@materia.route('/materia-prima')
@login_required
@roles_required('admin')
def materias():
    todas = MateriaPrima.query.order_by(MateriaPrima.idMateriaPrima.desc()).all()
    materias_proveidas = MateriaProveida.query.order_by(MateriaProveida.idMateriaProveida.desc()).all()
    categorias = Categoria.query.all()
    productos = Producto.query.all()
    proveedores = Proveedor.query.filter_by(estatus='activo').order_by(Proveedor.nombre).all()
    unidades = UnidadMedida.query.all()
    return render_template(
        'admin/materia/materia.html',
        materias=todas,
        materias_proveidas=materias_proveidas,
        categorias=categorias,
        productos=productos,
        proveedores=proveedores,
        unidades=unidades,
    )


@materia.route('/materia-prima/nueva', methods=['POST'])
@login_required
@roles_required('admin')
def materia_nueva():
    nombre = request.form.get('nombreMateriaPrima', '').strip()
    id_categoria = request.form.get('idCategoria') or None
    tipo = request.form.get('tipo')
    id_producto = request.form.get('idProducto') or None

    if tipo != 'Producto':
        id_producto = None

    if not nombre:
        flash('El nombre es obligatorio.', 'error')
        return redirect(url_for('materia.materias'))

    nueva = MateriaPrima(
        nombreMateriaPrima=nombre,
        idCategoria=int(id_categoria) if id_categoria else None,
        tipo=tipo,
        idProducto=int(id_producto) if id_producto else None,
    )
    db.session.add(nueva)
    try:
        db.session.commit()
        flash('Materia prima registrada correctamente.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash(f'Ya existe una materia prima con el nombre "{nombre}".', 'danger')
    return redirect(url_for('materia.materias'))


@materia.route('/materia-prima/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def materia_editar(id):
    mat = MateriaPrima.query.get_or_404(id)
    categorias = Categoria.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':
        nombre = request.form.get('nombreMateriaPrima', '').strip()
        if not nombre:
            flash('El nombre es obligatorio.', 'error')
            return render_template(
                'admin/materia/materia_form.html',
                materia=mat, categorias=categorias, productos=productos
            )
        mat.nombreMateriaPrima = nombre
        mat.idCategoria = int(request.form.get('idCategoria')) if request.form.get('idCategoria') else None
        mat.tipo = request.form.get('tipo')
        mat.idProducto = int(request.form.get('idProducto')) if request.form.get('idProducto') and mat.tipo == 'Producto' else None
        db.session.commit()
        flash('Materia prima actualizada correctamente.', 'success')
        return redirect(url_for('materia.materias'))

    return render_template(
        'admin/materia/materia_form.html',
        materia=mat,
        categorias=categorias,
        productos=productos,
    )


@materia.route('/materia-prima/<int:id>/eliminar', methods=['POST'])
@login_required
@roles_required('admin')
def materia_eliminar(id):
    mat = MateriaPrima.query.get_or_404(id)
    if mat.materiasProveidas.count() > 0:
        flash(
            f'No se puede eliminar "{mat.nombreMateriaPrima}" porque tiene '
            f'{mat.materiasProveidas.count()} materia(s) proveída(s) asignada(s). '
            'Elimínalas primero.',
            'danger'
        )
        return redirect(url_for('materia.materias'))
    db.session.delete(mat)
    try:
        db.session.commit()
        flash('Materia prima eliminada.', 'info')
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar porque tiene registros relacionados.', 'danger')
    return redirect(url_for('materia.materias'))


@materia.route('/materia-proveida/nueva', methods=['POST'])
@login_required
@roles_required('admin')
def materia_proveida_nueva():
    nombre = request.form.get('nombreMateriaProveida', '').strip()
    id_proveedor = request.form.get('idProveedor') or None
    id_materia = request.form.get('idMateriaPrima') or None
    id_unidad = request.form.get('idUnidadMedida') or None

    if not all([nombre, id_proveedor, id_materia, id_unidad]):
        flash('Todos los campos de materia proveida son obligatorios.', 'error')
        return redirect(url_for('materia.materias'))

    nueva = MateriaProveida(
        nombreMateriaProveida=nombre,
        idProveedor=int(id_proveedor),
        idMateriaPrima=int(id_materia),
        idUnidadMedida=int(id_unidad),
    )
    db.session.add(nueva)
    try:
        db.session.commit()
        flash('Materia proveida registrada correctamente.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash(f'Ya existe una materia proveida con el nombre "{nombre}".', 'danger')
    return redirect(url_for('materia.materias'))


@materia.route('/materia-proveida/<int:id>/eliminar', methods=['POST'])
@login_required
@roles_required('admin')
def materia_proveida_eliminar(id):
    mp = MateriaProveida.query.get_or_404(id)
    db.session.delete(mp)
    db.session.commit()
    flash('Materia proveida eliminada.', 'info')
    return redirect(url_for('materia.materias'))
