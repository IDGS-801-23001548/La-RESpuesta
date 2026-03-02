from flask import render_template, redirect, url_for, flash
from . import admin_bp
from app.extensions import db
from app.models import Usuario, Rol, Log, ModuloPermisos
from app.admin.forms import UserForm


@admin_bp.route("/", methods=['GET', 'POST'])
def dashboard():
    return render_template("admin/admin.html")


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

# ── RUTAS A DESARROLLAR ──────────────────────────────────────────

@admin_bp.route("/compras", methods=['GET', 'POST'])
def compras():
    return render_template("admin/compras.html")

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