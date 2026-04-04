from flask import render_template, redirect, url_for, flash, current_app, request
from . import user
from app.extensions import db
from app.models import User, Role, Persona
from app.modules.user.forms import UserForm
from flask_security import login_required, roles_required, hash_password, current_user, roles_accepted
import uuid

@user.route("/usuarios", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'Gerente')
def usuarios():
    usuarios_db = User.query.all()
    roles_db = Role.query.all()
    return render_template("admin/user/usuarios.html", usuarios_db=usuarios_db, roles_db=roles_db)

@user.route("/usuarios/nuevo", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def usuarios_nuevo():
    form = UserForm()
    form.id_rol.choices = [(r.id, r.name) for r in Role.query.all()]

    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            flash("Ya existe un usuario con ese correo.", "error")
            return render_template("admin/user/usuarios_nuevo.html", form=form)

        rol = Role.query.get(form.id_rol.data)

        # Construir nombre completo desde los tres campos
        nombre_completo = f"{form.nombre.data} {form.apellido_paterno.data} {form.apellido_materno.data}".strip()

        # Crear usuario
        nuevo_u = User(
            name=nombre_completo,
            email=form.email.data,
            password=hash_password(form.password.data),
            active=form.active.data,
            fs_uniquifier=uuid.uuid4().hex,
        )

        if rol:
            nuevo_u.roles.append(rol)

        db.session.add(nuevo_u)
        db.session.flush()

        # Crear persona vinculada al usuario
        nueva_persona = Persona(
            nombre=form.nombre.data,
            apellido_paterno=form.apellido_paterno.data,
            apellido_materno=form.apellido_materno.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            user_id=nuevo_u.id
        )

        db.session.add(nueva_persona)
        db.session.commit()

        flash("Usuario creado correctamente.", "success")
        current_app.logger.info(f"Usuario {form.email.data} creado — {nombre_completo}")
        return redirect(url_for("user.usuarios"))

    if form.errors:
        for campo, errores in form.errors.items():
            for error in errores:
                flash(error, "error")

    return render_template("admin/user/usuarios_nuevo.html", form=form)

@user.route("/usuarios/toggle_estatus/<int:id>", methods=["POST"])
@login_required
@roles_required('admin')
def usuarios_toggle_estatus(id):
    usuario = User.query.get_or_404(id)

    if usuario.id == current_user.id:
        flash("No puedes desactivar tu propio usuario.", "error")
        return redirect(url_for("user.usuarios"))

    anterior = usuario.active

    usuario.active = not usuario.active

    if usuario.active:
        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None

    db.session.commit()

    flash("Estatus actualizado correctamente", "success")

    current_app.logger.info(
        f"user = {usuario.name} {usuario.email} "
        f"estado: {anterior} -> {usuario.active} "
        f"desbloqueado={usuario.active} "
        f"cambiado por: {current_user.email}"
    )

    return redirect(url_for("user.usuarios"))

@user.route("/usuarios/<int:id>/eliminar", methods=["POST"])
@login_required
@roles_required('admin')
def usuarios_eliminar(id):
    usuario = User.query.get_or_404(id)
    persona = usuario.persona

    if usuario.id == current_user.id:
        flash("No puedes eliminar tu propio usuario.", "error")
        return redirect(url_for("user.usuarios"))

    try:
        db.session.delete(usuario)
        db.session.delete(persona)
        db.session.commit()
        flash("Usuario eliminado correctamente.", "success")
        current_app.logger.warning(f"user={usuario.name} {usuario.email} eliminado por {current_user.email} ")

    except Exception as e:
        db.session.rollback()
        flash("Error al eliminar el usuario.", "error")
        print(e)

    return redirect(url_for("user.usuarios"))

@user.route("/usuarios/<int:id>")
@login_required
@roles_required('admin')
def usuarios_detalles(id):
    usuario = User.query.get_or_404(id)
    return render_template("admin/user/usuarios_detalles.html", usuario=usuario)

@user.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def usuarios_editar(id):
    usuario = User.query.get_or_404(id)
    form = UserForm(obj=usuario)
    form.id_rol.choices = [(r.id, r.name) for r in Role.query.all()]

    # Pre-poblar campos de Persona en GET
    if request.method == 'GET' and usuario.persona:
        form.nombre.data          = usuario.persona.nombre
        form.apellido_paterno.data = usuario.persona.apellido_paterno
        form.apellido_materno.data = usuario.persona.apellido_materno
        form.telefono.data        = usuario.persona.telefono
        form.direccion.data       = usuario.persona.direccion
        # Pre-seleccionar rol actual
        if usuario.roles:
            form.id_rol.data = usuario.roles[0].id

    if form.validate_on_submit():

        # Verificar email duplicado (ignorando el propio usuario)
        email_existente = User.query.filter(
            User.email == form.email.data,
            User.id != usuario.id
        ).first()
        if email_existente:
            flash("Ya existe otro usuario con ese correo.", "error")
            return render_template("admin/user/usuarios_editar.html", form=form, usuario=usuario)

        # Actualizar datos de acceso
        usuario.email  = form.email.data
        usuario.active = form.active.data

        # Cambiar contraseña solo si se proporcionó una nueva
        if form.password.data:
            usuario.password = hash_password(form.password.data)

        # Actualizar rol
        rol = Role.query.get(form.id_rol.data)
        if rol:
            usuario.roles = [rol]

        # Actualizar nombre completo en User
        nombre_completo = f"{form.nombre.data} {form.apellido_paterno.data} {form.apellido_materno.data or ''}".strip()
        usuario.name = nombre_completo

        # Actualizar o crear Persona
        if usuario.persona:
            usuario.persona.nombre           = form.nombre.data
            usuario.persona.apellido_paterno = form.apellido_paterno.data
            usuario.persona.apellido_materno = form.apellido_materno.data
            usuario.persona.telefono         = form.telefono.data
            usuario.persona.direccion        = form.direccion.data
        else:
            nueva_persona = Persona(
                nombre           = form.nombre.data,
                apellido_paterno = form.apellido_paterno.data,
                apellido_materno = form.apellido_materno.data,
                telefono         = form.telefono.data,
                direccion        = form.direccion.data,
                user_id          = usuario.id
            )
            db.session.add(nueva_persona)

        db.session.commit()

        flash("Usuario actualizado correctamente.", "success")
        current_app.logger.info(f"Usuario {usuario.email} actualizado por {current_user.email}")
        return redirect(url_for("user.usuarios_detalles", id=usuario.id))

    if form.errors:
        for campo, errores in form.errors.items():
            for error in errores:
                flash(error, "error")

    return render_template("admin/user/usuarios_editar.html", form=form, usuario=usuario)

# ─────────────────────────────────────────────────────────────────────────────
#  REGISTRO PÚBLICO DE CLIENTE
#  Ruta abierta (sin @login_required). Crea siempre usuarios con el rol
#  cuyo id sea 5 (Cliente), reutilizando la misma lógica que usuarios_nuevo.
# ─────────────────────────────────────────────────────────────────────────────

@user.route("/registro", methods=["GET"])
def registro_cliente():
    """Muestra el formulario de registro público para clientes."""
    from app.modules.user.forms import RegistroClienteForm
    form = RegistroClienteForm()
    return render_template("admin/user/registro_cliente.html", form=form)


@user.route("/registro", methods=["POST"])
def registro_cliente_post():
    """Procesa el registro público. Asigna siempre el rol con id=5 (Cliente)."""
    from app.modules.user.forms import RegistroClienteForm

    form = RegistroClienteForm()

    if not form.validate_on_submit():
        for campo, errores in form.errors.items():
            for error in errores:
                flash(error, "error")
        return render_template("admin/user/registro_cliente.html", form=form)

    # Correo duplicado
    if User.query.filter_by(email=form.email.data).first():
        flash("Ya existe una cuenta con ese correo.", "error")
        return render_template("admin/user/registro_cliente.html", form=form)

    # Rol Cliente (id = 5)
    rol_cliente = Role.query.get(5)
    if not rol_cliente:
        flash("Error de configuración: el rol de cliente no existe. Contacta al administrador.", "error")
        current_app.logger.error("Registro público fallido: Role id=5 (Cliente) no encontrado en BD")
        return render_template("admin/user/registro_cliente.html", form=form)

    nombre_completo = f"{form.nombre.data} {form.apellido_paterno.data} {form.apellido_materno.data or ''}".strip()

    nuevo_u = User(
        name=nombre_completo,
        email=form.email.data,
        password=hash_password(form.password.data),
        active=True,
        fs_uniquifier=uuid.uuid4().hex,
    )
    nuevo_u.roles.append(rol_cliente)

    db.session.add(nuevo_u)
    db.session.flush()  # obtiene nuevo_u.id antes del commit

    nueva_persona = Persona(
        nombre=form.nombre.data,
        apellido_paterno=form.apellido_paterno.data,
        apellido_materno=form.apellido_materno.data,
        telefono=form.telefono.data,
        direccion=form.direccion.data,
        user_id=nuevo_u.id
    )

    db.session.add(nueva_persona)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al registrar cliente: {str(e)}")
        flash("Ocurrió un error al crear tu cuenta. Intenta de nuevo.", "error")
        return render_template("admin/user/registro_cliente.html", form=form)

    current_app.logger.info(f"Cliente registrado públicamente: {form.email.data}")
    flash("¡Cuenta creada exitosamente! Ya puedes iniciar sesión.", "success")
    return redirect(url_for("auth.login"))
