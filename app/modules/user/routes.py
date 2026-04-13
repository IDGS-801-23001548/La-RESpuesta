from flask import render_template, redirect, url_for, flash, current_app, request, session
from . import user
from app.extensions import db
from app.models import User, Role, Persona
from app.modules.user.forms import UserForm
from flask_security import login_required, roles_required, hash_password, current_user, roles_accepted
import uuid
from flask_mail import Message
from app.extensions import mail
import random
from datetime import datetime, timedelta

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
        email_admin = current_user.email if current_user and current_user.is_authenticated else 'sistema'
        current_app.logger.info(
            f"Usuario creado | email={form.email.data} | nombre={nombre_completo} "
            f"| rol={rol.name if rol else '—'} | creado_por={email_admin} "
            f"| ip={request.remote_addr}"
        )
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
        f"Usuario estado: {anterior} -> {usuario.active} | email={usuario.email} "
        f"| nombre={usuario.name} | desbloqueado={usuario.active} "
        f"| cambiado_por={current_user.email} | ip={request.remote_addr}"
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
        current_app.logger.warning(
            f"Usuario eliminado | email={usuario.email} | nombre={usuario.name} "
            f"| eliminado_por={current_user.email} | ip={request.remote_addr}"
        )

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
        current_app.logger.info(
            f"Usuario actualizado | email={usuario.email} | nombre={usuario.name} "
            f"| actualizado_por={current_user.email} | ip={request.remote_addr}"
        )
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
        flash("Error de configuración: el rol de cliente no existe.", "error")
        current_app.logger.error("Registro público fallido: Role id=5 no encontrado")
        return render_template("admin/user/registro_cliente.html", form=form)

    # ── Guardar datos en sesión temporalmente ──────────────────
    session['registro_pendiente'] = {
        'nombre':           form.nombre.data,
        'apellido_paterno': form.apellido_paterno.data,
        'apellido_materno': form.apellido_materno.data or '',
        'telefono':         form.telefono.data,
        'direccion':        form.direccion.data,
        'email':            form.email.data,
        'password':         form.password.data,
    }

    # ── Generar y enviar código ────────────────────────────────
    codigo = str(random.randint(100000, 999999))
    expira = datetime.now() + timedelta(minutes=5)

    session['registro_2fa_codigo'] = codigo
    session['registro_2fa_expira'] = expira.isoformat()
    session.modified = True

    nombre = form.nombre.data

    try:
        msg = Message(
            subject='Confirma tu cuenta — La RESpuesta',
            recipients=[form.email.data],
            html=f"""
            <div style="font-family:Inter,sans-serif;max-width:420px;margin:0 auto;padding:32px 24px;">
              <h2 style="color:#111827;font-size:1.25rem;margin-bottom:8px;">
                Confirma tu cuenta
              </h2>
              <p style="color:#6b7280;font-size:.875rem;margin-bottom:24px;">
                Hola {nombre}, usa el siguiente código para completar tu registro.
                Expira en <strong>5 minutos</strong>.
              </p>
              <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;
                          padding:24px;text-align:center;margin-bottom:24px;">
                <span style="font-size:2.25rem;font-weight:700;letter-spacing:.25em;color:#16a34a;">
                  {codigo}
                </span>
              </div>
              <p style="color:#9ca3af;font-size:.75rem;">
                Si no solicitaste este código, ignora este mensaje.
              </p>
            </div>
            """
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error enviando código de registro | {str(e)}")
        flash("Error al enviar el código de verificación. Intenta de nuevo.", "error")
        return render_template("admin/user/registro_cliente.html", form=form)

    return redirect(url_for("user.verificar_registro"))


@user.route("/registro/verificar", methods=["GET"])
def verificar_registro():
    if 'registro_pendiente' not in session:
        return redirect(url_for("user.registro_cliente"))
    return render_template("admin/user/verificar_registro.html")


@user.route("/registro/verificar", methods=["POST"])
def verificar_registro_post():
    from flask_security.utils import hash_password

    if 'registro_pendiente' not in session:
        return redirect(url_for("user.registro_cliente"))

    codigo_ingresado = request.form.get('codigo', '').strip()
    codigo_guardado  = session.get('registro_2fa_codigo')
    expira_str       = session.get('registro_2fa_expira')

    # ── Verificar expiración ──────────────────────────────────
    if not expira_str or datetime.now() > datetime.fromisoformat(expira_str):
        session.pop('registro_pendiente', None)
        session.pop('registro_2fa_codigo', None)
        session.pop('registro_2fa_expira', None)
        session.modified = True
        flash("El código ha expirado. Vuelve a registrarte.", "error")
        return redirect(url_for("user.registro_cliente"))

    # ── Verificar código ──────────────────────────────────────
    if codigo_ingresado != codigo_guardado:
        flash("Código incorrecto. Intenta de nuevo.", "error")
        return redirect(url_for("user.verificar_registro"))

    # ── Código correcto — crear la cuenta ─────────────────────
    datos = session['registro_pendiente']
    rol_cliente = Role.query.get(5)

    nombre_completo = f"{datos['nombre']} {datos['apellido_paterno']} {datos['apellido_materno']}".strip()

    nuevo_u = User(
        name         = nombre_completo,
        email        = datos['email'],
        password     = hash_password(datos['password']),
        active       = True,
        fs_uniquifier= uuid.uuid4().hex,
    )
    nuevo_u.roles.append(rol_cliente)
    db.session.add(nuevo_u)
    db.session.flush()

    nueva_persona = Persona(
        nombre           = datos['nombre'],
        apellido_paterno = datos['apellido_paterno'],
        apellido_materno = datos['apellido_materno'],
        telefono         = datos['telefono'],
        direccion        = datos['direccion'],
        user_id          = nuevo_u.id
    )
    db.session.add(nueva_persona)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al crear cuenta verificada: {str(e)}")
        flash("Error al crear la cuenta. Intenta de nuevo.", "error")
        return redirect(url_for("user.registro_cliente"))

    # Limpiar sesión de registro
    session.pop('registro_pendiente', None)
    session.pop('registro_2fa_codigo', None)
    session.pop('registro_2fa_expira', None)
    session.modified = True

    current_app.logger.info(
        f"Cliente registrado con verificacion | email={datos['email']} "
        f"| nombre={nombre_completo} | ip={request.remote_addr}"
    )
    flash("¡Cuenta creada exitosamente! Ya puedes iniciar sesión.", "success")
    return redirect(url_for("auth.login"))


@user.route("/registro/verificar/reenviar", methods=["POST"])
def reenviar_registro():
    if 'registro_pendiente' not in session:
        return redirect(url_for("user.registro_cliente"))

    datos  = session['registro_pendiente']
    codigo = str(random.randint(100000, 999999))
    expira = datetime.now() + timedelta(minutes=5)

    session['registro_2fa_codigo'] = codigo
    session['registro_2fa_expira'] = expira.isoformat()
    session.modified = True

    try:
        msg = Message(
            subject='Nuevo código de verificación — La RESpuesta',
            recipients=[datos['email']],
            html=f"""
            <div style="font-family:Inter,sans-serif;max-width:420px;margin:0 auto;padding:32px 24px;">
              <h2 style="color:#111827;font-size:1.25rem;margin-bottom:8px;">Nuevo código</h2>
              <p style="color:#6b7280;font-size:.875rem;margin-bottom:24px;">
                Tu nuevo código de verificación. Expira en <strong>5 minutos</strong>.
              </p>
              <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;
                          padding:24px;text-align:center;">
                <span style="font-size:2.25rem;font-weight:700;letter-spacing:.25em;color:#16a34a;">
                  {codigo}
                </span>
              </div>
            </div>
            """
        )
        mail.send(msg)
        flash("Código reenviado correctamente.", "success")
    except Exception as e:
        current_app.logger.error(f"Error reenviando código de registro | {str(e)}")
        flash("Error al reenviar el código.", "error")

    return redirect(url_for("user.verificar_registro"))