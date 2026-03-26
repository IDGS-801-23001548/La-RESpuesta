from flask import render_template, redirect, url_for, flash, request
from . import user
from app.extensions import db
from app.models import User, Role, ModuloPermisos
from app.user.forms import UserForm
from flask_login import current_user
from flask import abort

@user.route("/usuarios")
def usuarios():
    if not current_user.tiene_permiso("Usuarios", "read"):
        abort(403)

    usuarios_db = User.query.all()
    return render_template("admin/user/usuarios.html", usuarios_db=usuarios_db)

@user.route("/usuarios/nuevo", methods=["GET", "POST"])
def usuarios_nuevo():

    if not current_user.tiene_permiso("Usuarios", "create"):
        abort(403)
        
    form = UserForm()
    form.id_rol.choices = [(r.id_rol, r.nombre_rol) for r in Role.query.all()]

    permisos_por_rol = {}
    for permiso in ModuloPermisos.query.all():
        permisos_por_rol.setdefault(str(permiso.id_rol), []).append({
            "modulo":        permiso.modulo,
            "l_lectura":     permiso.l_lectura,
            "a_alta":        permiso.a_alta,
            "b_baja":        permiso.b_baja,
            "m_modificacion":permiso.m_modificacion,
        })

    if form.validate_on_submit():
        nuevo_u = User(
            nombre_usuario=form.username.data,
            id_rol=form.id_rol.data
        )
        nuevo_u.set_password(form.password.data)
        nuevo_u.estatus = 'Activo' if form.estatus.data else 'Inactivo'
        db.session.add(nuevo_u)
        i = 0
        while f"modulo_{i}" in request.form:
            modulo = request.form.get(f"modulo_{i}")
            p = ModuloPermisos(
                id_rol          = form.id_rol.data,
                modulo          = modulo,
                l_lectura       = bool(request.form.get(f"perm_{i}_l_lectura")),
                a_alta          = bool(request.form.get(f"perm_{i}_a_alta")),
                b_baja          = bool(request.form.get(f"perm_{i}_b_baja")),
                m_modificacion  = bool(request.form.get(f"perm_{i}_m_modificacion")),
            )
            db.session.add(p)
            i += 1
        db.session.commit()
        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("admin.usuarios"))

    # Si hay errores de validación, mostrarlos como flash
    if form.errors:
        for campo, errores in form.errors.items():
            for error in errores:
                flash(error, "error")

    return render_template("admin/user/usuarios_nuevo.html", form=form, permisos_por_rol=permisos_por_rol)

@user.route("/editar")
def usuarios_editar():
    return(f"AGREGAR EDITAR")

@user.route("/editar_estatus")
def usuarios_toggle_estatus():
    return(f"AGREGAR usuarios_toggle_estatus")