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
from app.models import MateriaPrima, MateriaProveida, Lote, Categoria
from sqlalchemy import func


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

@materia.route('/inventario')
@login_required
@roles_required('admin')
def inventario():
    materias = MateriaPrima.query.order_by(MateriaPrima.nombreMateriaPrima).all()
    categorias = Categoria.query.all()

    # ── Calcular stock por MateriaPrima ─────────────────────────────────────
    # Stock disponible = sum(totalMateria) de MPU con estatus='Disponible'
    # agrupado por idMateriaPrima a través de MateriaProveida
    stock_query = (
        db.session.query(
            MateriaProveida.idMateriaPrima,
            func.sum(Lote.totalMateria).label('stock_total'),
            func.sum(Lote.totalCosto).label('costo_total'),
            func.count(Lote.idLote).label('n_lotes'),
        )
        .join(Lote,
              Lote.idMateriaProveida == MateriaProveida.idMateriaProveida)
        .filter(Lote.estatus == 'Disponible')
        .group_by(MateriaProveida.idMateriaPrima)
        .all()
    )

    # Convertir a dict keyed por idMateriaPrima
    stock_map = {
        row.idMateriaPrima: {
            'stock_total': row.stock_total or 0,
            'costo_total': row.costo_total or 0.0,
            'n_lotes':     row.n_lotes or 0,
            # Costo promedio por unidad de conversor
            'costo_promedio': (float(row.costo_total) / float(row.stock_total))
            if row.stock_total and row.stock_total > 0 else 0.0
        }
        for row in stock_query
    }

    # Calcular totales generales para KPI cards
    total_valor = sum(v['costo_total'] for v in stock_map.values())
    total_lotes = sum(v['n_lotes']     for v in stock_map.values())

    return render_template(
        'admin/materia/inventario_materias.html',
        materias=materias,
        categorias=categorias,
        stock_map=stock_map,
        total_valor=total_valor,
        total_lotes=total_lotes,
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
