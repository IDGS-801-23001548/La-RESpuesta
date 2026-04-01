<<<<<<< HEAD
from flask import render_template, redirect, url_for, flash
from . import admin_bp
from app.extensions import db
from app.models import Usuario, Rol, Log, ModuloPermisos
from app.admin.forms import UserForm


@admin_bp.route("/", methods=['GET', 'POST'])
def dashboard():
    return render_template("admin/admin.html")
=======
from flask import render_template, redirect, url_for, flash, request
from . import admin_bp
from app.extensions import db
from app.models import Usuario, Rol, Log, ModuloPermisos
from app.admin.forms import UserForm, ComprasForm


@admin_bp.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template("admin/dashboard.html")
>>>>>>> develop


@admin_bp.route("/usuarios", methods=['GET'])
def usuarios():
    usuarios_db = Usuario.query.all()
    return render_template("admin/usuarios.html", usuarios_db=usuarios_db)


@admin_bp.route("/usuarios/nuevo", methods=["GET", "POST"])
def usuarios_nuevo():
    form = UserForm()
    form.id_rol.choices = [(r.id_rol, r.nombre_rol) for r in Rol.query.all()]

    if form.validate_on_submit():
        nuevo_u = Usuario(
            nombre_usuario=form.username.data,
            id_rol=form.id_rol.data
        )
        nuevo_u.set_password(form.password.data)
        nuevo_u.estatus = 'Activo' if form.estatus.data else 'Inactivo'
        db.session.add(nuevo_u)
        db.session.commit()
        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("admin.usuarios"))

    # Si hay errores de validación, mostrarlos como flash
    if form.errors:
        for campo, errores in form.errors.items():
            for error in errores:
                flash(error, "error")

    return render_template("admin/usuarios_nuevo.html", form=form)

<<<<<<< HEAD
# ── RUTAS A DESARROLLAR ──────────────────────────────────────────
=======
>>>>>>> develop

@admin_bp.route("/compras", methods=['GET', 'POST'])
def compras():
    return render_template("admin/compras.html")

<<<<<<< HEAD
@admin_bp.route("/materia", methods=['GET', 'POST'])
def materia():
    return render_template("admin/materia.html")

@admin_bp.route("/recetas", methods=['GET', 'POST'])
def recetas():
    return render_template("admin/recetas.html")

@admin_bp.route("/produccion", methods=['GET', 'POST'])
def produccion():
    return render_template("admin/produccion.html")

@admin_bp.route("/solicitud", methods=['GET', 'POST'])
def solicitud():
    return render_template("admin/solicitud.html")

@admin_bp.route("/productos", methods=['GET', 'POST'])
def productos():
    return render_template("admin/productos.html")

@admin_bp.route("/ventas", methods=['GET', 'POST'])
def ventas():
    return render_template("admin/ventas.html")

@admin_bp.route("/pago", methods=['GET', 'POST'])
def pago():
    return render_template("admin/pago.html")

@admin_bp.route("/corte", methods=['GET', 'POST'])
def corte():
    return render_template("admin/corte.html")
=======
@admin_bp.route("/compras/detalle", methods=['GET', 'POST'])
def compras_detalle():
    return render_template("admin/compras.html")

@admin_bp.route("/compras/nueva", methods=['GET', 'POST'])
def compras_nueva():
    form = ComprasForm()
    return render_template("admin/compras_nueva.html", form = form)

@admin_bp.route('/materia-prima')
def materia():
    return render_template('admin/materia.html')

@admin_bp.route('/materia-prima/nueva')
def materia_nueva():
    return render_template('admin/materia_form.html', materia=None)

@admin_bp.route('/materia-prima/<int:id>/editar')
def materia_editar(id):
    return render_template('admin/materia_form.html', materia=None)

@admin_bp.route('/materia-prima/<int:id>/eliminar', methods=['POST'])
def materia_eliminar(id):
    return redirect(url_for('materia'))

@admin_bp.route('/proveedores')
def proveedores():
    return render_template('admin/proveedores.html')

@admin_bp.route('/proveedores/nuevo')
def proveedores_nuevo():
    form = UserForm()
    return render_template('admin/proveedores_form.html', proveedor=None, form = form)

@admin_bp.route('/proveedores/detalle')
def proveedores_detalle():
    return render_template('admin/proveedores_detalle.html', proveedor=None)

@admin_bp.route('/proveedores/<int:id>/editar')
def proveedores_editar(id):
    form = ComprasForm()
    return render_template('admin/proveedores_form.html', proveedor=None, form = form)

@admin_bp.route('/proveedores/<int:id>/eliminar', methods=['POST'])
def proveedores_eliminar(id):
    return redirect(url_for('proveedores'))

@admin_bp.route('/recetas')
def recetas():
    return render_template('admin/recetas.html', recetas=[])

@admin_bp.route('/recetas/nueva')
def recetas_nueva():
    return render_template('admin/recetas_form.html', receta=None)

@admin_bp.route('/recetas/<int:id>/editar')
def recetas_editar(id):
    return render_template('admin/recetas_form.html', receta=None)

@admin_bp.route('/recetas/<int:id>/eliminar', methods=['POST'])
def recetas_eliminar(id):
    return redirect(url_for('recetas'))

@admin_bp.route('/solicitudes')
def solicitudes():
    return render_template('admin/solicitudes.html', solicitudes=[])

@admin_bp.route('/solicitudes/nueva')
def solicitudes_nueva():
    return render_template('admin/solicitudes_form.html', solicitud=None)

@admin_bp.route('/solicitudes/<int:id>/editar')
def solicitudes_editar(id):
    return render_template('admin/solicitudes_form.html', solicitud=None)

@admin_bp.route('/solicitudes/<int:id>/cancelar', methods=['POST'])
def solicitudes_cancelar(id):
    return redirect(url_for('admin_bp.solicitudes'))

@admin_bp.route('/produccion')
def produccion():
    return render_template('admin/produccion.html',
                           ordenes=[], solicitudes_pendientes=[], kg_producidos=0)

@admin_bp.route('/produccion/nueva')
def produccion_nueva():
    return render_template('admin/produccion_form.html', solicitud=None)

@admin_bp.route('/produccion/desde-solicitud/<int:id>')
def produccion_desde_solicitud(id):
    return render_template('admin/produccion_form.html', solicitud=None)

@admin_bp.route('/produccion/<int:id>')
def produccion_detalle(id):
    return render_template('admin/produccion_detalle.html', orden=None)

@admin_bp.route('/produccion/<int:id>/completar', methods=['GET', 'POST'])
def produccion_completar(id):
    return redirect(url_for('admin.produccion_detalle', id=id))


@admin_bp.route('/productos')
def productos():
    return render_template('admin/productos.html',
                           productos=[], kg_totales=0)

@admin_bp.route('/productos/ajuste', methods=['GET', 'POST'])
def productos_ajuste():
    return render_template('admin/productos_ajuste.html', producto=None)

@admin_bp.route('/ventas')
def ventas():
    return render_template('admin/ventas.html',
        ventas=[],
        total_hoy='0.00',
        tickets_hoy=0,
        kg_hoy=0,
        ticket_promedio='0.00',
        ventas_por_canal={},
        tickets_por_canal={}
    )


@admin_bp.route('/pago')
def pago():
    return render_template('admin/pagos.html',
        proveedores=[], pagos=[],
        total_pendiente='0.00', proveedores_con_saldo=0,
        pagado_mes='0.00', num_pagos_mes=0)

@admin_bp.route('/pagos/nuevo', methods=['GET', 'POST'])
def pagos_nuevo():
    proveedor_id = request.args.get('proveedor_id')
    return render_template('admin/pagos_form.html', proveedor_id=proveedor_id)

@admin_bp.route('/pagos/proveedor/<int:id>')
def pagos_cuenta(id):
    return render_template('admin/pagos_cuenta.html',
        proveedor=None, movimientos=[])

@admin_bp.route('/corte')
def corte_diario():
    return render_template('admin/corte_diario.html',
        cortes=[],
        corte_hoy_existe=False,
        corte_hoy_id=None,
        ventas_mes='0.00',
        utilidad_mes='0.00',
        dias_sin_corte=0
    )

@admin_bp.route('/corte/diario/<int:id>')
def corte_detalle(id):
    return render_template('admin/corte_detalle.html', corte=None)

@admin_bp.route('/corte-diario/generar', methods=['POST'])
def corte_generar():
    return redirect(url_for('admin.corte_diario'))

# ── RUTAS A DESARROLLAR ──────────────────────────────────────────
>>>>>>> develop

@admin_bp.route("/utilidad", methods=['GET', 'POST'])
def utilidad():
    return render_template("admin/utilidad.html")

@admin_bp.route("/reportes", methods=['GET', 'POST'])
def reportes():
    return render_template("admin/reportes.html")

@admin_bp.route("/logs", methods=['GET', 'POST'])
def logs():
    return render_template("admin/logs.html")

@admin_bp.route("/ajustes", methods=['GET', 'POST'])
def ajustes():
    return render_template("admin/ajustes.html")