from flask import render_template, redirect, url_for, flash, request
from . import proveedor
from .forms import ProveedorForm
from app.extensions import db
from app.models.proveedor import Proveedor
from flask_login import login_required
from flask_security import roles_required


@proveedor.route('/proveedores')
@login_required
@roles_required('admin')
def proveedores():
    todos = Proveedor.query.order_by(Proveedor.nombre).all()
    return render_template('admin/proveedores/proveedores.html', proveedores=todos)


@proveedor.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def proveedores_nuevo():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo = Proveedor(
            nombre         = form.nombre.data.strip(),
            rfc            = form.rfc.data.strip().upper(),
            estatus        = form.estatus.data,
            contacto       = form.contacto.data.strip(),
            telefono       = form.telefono.data.strip(),
            correo         = form.correo.data.strip() or None,
            direccion      = form.direccion.data.strip() or None,
            productos      = ','.join(form.productos.data),
            condicion_pago = form.condicion_pago.data,
            dias_entrega   = ','.join(form.dias_entrega.data) if form.dias_entrega.data else None,
            notas          = form.notas.data.strip() or None,
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Proveedor registrado correctamente.', 'success')
        return redirect(url_for('proveedor.proveedores'))
    return render_template('admin/proveedores/proveedores_form.html', proveedor=None, form=form)


@proveedor.route('/proveedores/<int:id>/detalle')
@login_required
@roles_required('admin')
def proveedores_detalle(id):
    prov = Proveedor.query.get_or_404(id)
    return render_template('admin/proveedores/proveedores_detalle.html', proveedor=prov)


@proveedor.route('/proveedores/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def proveedores_editar(id):
    prov = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=prov)

    if request.method == 'GET':
        # Convertir las cadenas almacenadas a listas para preseleccionar checkboxes
        form.productos.data    = prov.productos_lista
        form.dias_entrega.data = prov.dias_entrega_lista

    if form.validate_on_submit():
        prov.nombre         = form.nombre.data.strip()
        prov.rfc            = form.rfc.data.strip().upper()
        prov.estatus        = form.estatus.data
        prov.contacto       = form.contacto.data.strip()
        prov.telefono       = form.telefono.data.strip()
        prov.correo         = form.correo.data.strip() or None
        prov.direccion      = form.direccion.data.strip() or None
        prov.productos      = ','.join(form.productos.data)
        prov.condicion_pago = form.condicion_pago.data
        prov.dias_entrega   = ','.join(form.dias_entrega.data) if form.dias_entrega.data else None
        prov.notas          = form.notas.data.strip() or None
        db.session.commit()
        flash('Proveedor actualizado correctamente.', 'success')
        return redirect(url_for('proveedor.proveedores_detalle', id=prov.id))

    return render_template('admin/proveedores/proveedores_form.html', proveedor=prov, form=form)


@proveedor.route('/proveedores/<int:id>/eliminar', methods=['POST'])
@login_required
@roles_required('admin')
def proveedores_eliminar(id):
    prov = Proveedor.query.get_or_404(id)
    db.session.delete(prov)
    db.session.commit()
    flash('Proveedor eliminado.', 'info')
    return redirect(url_for('proveedor.proveedores'))


@proveedor.route('/proveedores/<int:id>/toggle', methods=['POST'])
@login_required
@roles_required('admin')
def proveedores_toggle(id):
    """Activa o desactiva un proveedor.
    La logica de bloqueo (no asociar a nuevas ordenes si esta inactivo)
    debe verificarse en las rutas de compras usando proveedor.es_activo.
    """
    prov = Proveedor.query.get_or_404(id)
    prov.estatus = 'inactivo' if prov.es_activo else 'activo'
    db.session.commit()
    return redirect(url_for('proveedor.proveedores'))


# ── Rutas de compras (pendientes de implementar) ──────────────────────

@proveedor.route('/proveedores/compra_nueva')
@login_required
@roles_required('admin')
def compras_nueva():
    return 'compra nueva'


@proveedor.route('/proveedores/compras')
@login_required
@roles_required('admin')
def compras():
    return 'Historial de compras'


@proveedor.route('/proveedores/compras/<int:id>/detalle')
@login_required
@roles_required('admin')
def compras_detalle(id):
    return f'Detalle compra {id}'
