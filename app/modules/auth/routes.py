from flask import request, render_template, redirect, url_for, flash, current_app, session
from flask_login import current_user
from flask_security.utils import login_user, logout_user, verify_password, hash_password
from flask_mail import Message
from app.models import User
from app.extensions import db, limiter, limit_by_email, mail
from app import user_datastore
from flask_security import login_required
from . import auth
from datetime import datetime, timedelta
import uuid
import random


# ─────────────────────────────────────────────────────────────
#  HELPER — determinar si el usuario requiere 2FA
# ─────────────────────────────────────────────────────────────
def _requiere_2fa(user):
    """
    Empleados (Cajero, admin, etc.) siempre requieren 2FA.
    Clientes (end-user) solo si tienen activada la opción.
    """
    roles_empleado = {'admin', 'Cajero'}
    roles_usuario  = {r.name for r in user.roles}

    if roles_empleado & roles_usuario:
        return True

    if 'end-user' in roles_usuario and user.autenticacion_doble_factor:
        return True

    return False


# ─────────────────────────────────────────────────────────────
#  HELPER — generar y enviar código 2FA
# ─────────────────────────────────────────────────────────────
def _enviar_codigo_2fa(user):
    codigo = str(random.randint(100000, 999999))
    expira = datetime.now() + timedelta(minutes=5)

    session['2fa_user_id']  = user.id
    session['2fa_codigo']   = codigo
    session['2fa_expira']   = expira.isoformat()
    session.modified = True

    msg = Message(
        subject='Tu código de verificación — La RESpuesta',
        recipients=[user.email],
        html=f"""
        <div style="font-family:Inter,sans-serif;max-width:420px;margin:0 auto;padding:32px 24px;">
          <h2 style="color:#111827;font-size:1.25rem;margin-bottom:8px;">
            Verificación de identidad
          </h2>
          <p style="color:#6b7280;font-size:.875rem;margin-bottom:24px;">
            Hola {user.name}, usa el siguiente código para completar tu inicio de sesión.
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
            Tu cuenta sigue segura.
          </p>
        </div>
        """
    )
    mail.send(msg)


# ─────────────────────────────────────────────────────────────
#  LOGIN GET
# ─────────────────────────────────────────────────────────────
@auth.route("/login")
def login():
    if current_user.is_authenticated:
        if current_user.has_role('admin'):
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('venta.inicio'))

    return render_template("security/login_user.html")


# ─────────────────────────────────────────────────────────────
#  LOGIN POST
# ─────────────────────────────────────────────────────────────
@auth.route("/login", methods=['POST'])
@limiter.limit("5 per minute")
@limiter.limit("3 per minute", key_func=limit_by_email)
def login_post():
    email    = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # ── Cuenta bloqueada ──────────────────────────────────────
    if user and user.bloqueado_hasta:
        if datetime.now() < user.bloqueado_hasta:
            current_app.logger.warning(
                f"Intento en cuenta bloqueada | email={email} | ip={request.remote_addr}"
            )
            flash("Cuenta bloqueada temporalmente. Intenta más tarde.", "error")
            return redirect(url_for("auth.login"))

    is_valid = user and verify_password(password, user.password)

    # ── Credenciales incorrectas ──────────────────────────────
    if not is_valid:
        if user:
            user.intentos_fallidos = (user.intentos_fallidos or 0) + 1

            if user.intentos_fallidos >= 5 and not user.bloqueado_hasta:
                user.bloqueado_hasta = datetime.now() + timedelta(minutes=10)
                user.active          = 0
                current_app.logger.warning(
                    f"Usuario bloqueado por intentos | email={email}"
                )

            db.session.commit()

        current_app.logger.warning(
            f"Intento fallido | email={email} | ip={request.remote_addr}"
        )
        flash("El usuario y/o la contraseña son incorrectos", "error")
        return redirect(url_for("auth.login"))

    # ── Credenciales correctas — guardar remember para usarlo tras 2FA ──
    session['2fa_remember'] = remember

    # ── ¿Requiere 2FA? ───────────────────────────────────────
    if _requiere_2fa(user):
        try:
            _enviar_codigo_2fa(user)
        except Exception as e:
            current_app.logger.error(f"Error enviando 2FA | email={email} | {str(e)}")
            flash("Error al enviar el código de verificación. Intenta de nuevo.", "error")
            return redirect(url_for("auth.login"))

        current_app.logger.info(f"Código 2FA enviado | email={email}")
        return redirect(url_for("auth.verificar_2fa"))

    # ── Sin 2FA — login directo ───────────────────────────────
    return _completar_login(user, remember)


# ─────────────────────────────────────────────────────────────
#  VERIFICACIÓN 2FA — GET
# ─────────────────────────────────────────────────────────────
@auth.route("/verificar", methods=['GET'])
def verificar_2fa():
    # Si no hay sesión 2FA pendiente, redirigir al login
    if '2fa_user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template("security/verificar_2fa.html")


# ─────────────────────────────────────────────────────────────
#  VERIFICACIÓN 2FA — POST
# ─────────────────────────────────────────────────────────────
@auth.route("/verificar", methods=['POST'])
def verificar_2fa_post():
    if '2fa_user_id' not in session:
        return redirect(url_for('auth.login'))

    codigo_ingresado = request.form.get('codigo', '').strip()
    codigo_guardado  = session.get('2fa_codigo')
    expira_str       = session.get('2fa_expira')
    user_id          = session.get('2fa_user_id')
    remember         = session.get('2fa_remember', False)

    # ── Verificar expiración ──────────────────────────────────
    if not expira_str or datetime.now() > datetime.fromisoformat(expira_str):
        _limpiar_sesion_2fa()
        flash("El código ha expirado. Inicia sesión de nuevo.", "error")
        return redirect(url_for("auth.login"))

    # ── Verificar código ──────────────────────────────────────
    if codigo_ingresado != codigo_guardado:
        flash("Código incorrecto. Intenta de nuevo.", "error")
        return redirect(url_for("auth.verificar_2fa"))

    # ── Código correcto ───────────────────────────────────────
    user = User.query.get(user_id)
    if not user:
        _limpiar_sesion_2fa()
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("auth.login"))

    _limpiar_sesion_2fa()
    return _completar_login(user, remember)


# ─────────────────────────────────────────────────────────────
#  REENVIAR CÓDIGO
# ─────────────────────────────────────────────────────────────
@auth.route("/verificar/reenviar", methods=['POST'])
def reenviar_codigo():
    user_id = session.get('2fa_user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    try:
        _enviar_codigo_2fa(user)
        flash("Código reenviado correctamente.", "success")
    except Exception as e:
        current_app.logger.error(f"Error reenviando 2FA | id={user_id} | {str(e)}")
        flash("Error al reenviar el código. Intenta de nuevo.", "error")

    return redirect(url_for("auth.verificar_2fa"))


# ─────────────────────────────────────────────────────────────
#  HELPERS INTERNOS
# ─────────────────────────────────────────────────────────────
def _limpiar_sesion_2fa():
    for key in ('2fa_user_id', '2fa_codigo', '2fa_expira', '2fa_remember'):
        session.pop(key, None)
    session.modified = True


def _completar_login(user, remember):
    """Registra auditoría, hace login y redirige según rol."""
    user.session_token      = str(uuid.uuid4())
    user.session_expiration = (
        datetime.now() + timedelta(days=7)
        if remember
        else datetime.now() + timedelta(minutes=10)
    )
    user.ultima_sesion     = datetime.now()
    user.ultima_ip         = request.remote_addr
    user.intentos_fallidos = 0
    user.bloqueado_hasta   = None

    session["session_token"] = user.session_token
    session["remember_me"]   = remember

    db.session.commit()

    login_user(user, remember=remember)
    session.permanent = True

    current_app.logger.info(
        f"Login exitoso | email={user.email} | ip={request.remote_addr}"
    )

    if user.has_role('admin'):
        return redirect(url_for('admin.dashboard'))

    if user.has_role('Cajero'):
        return redirect(url_for('mostrador.mostradorVenta'))

    if user.has_role('end-user'):
        return redirect(url_for('venta.inicio'))

    current_app.logger.warning(f"Usuario sin rol reconocido | email={user.email}")
    return redirect(url_for('venta.inicio'))


# ─────────────────────────────────────────────────────────────
#  REGISTER
# ─────────────────────────────────────────────────────────────
@auth.route("/register")
def register():
    return render_template("security/register.html")


@auth.route("/register", methods=['POST'])
def register_post():
    email    = request.form.get('email')
    name     = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Ya existe un usuario con este email", "warning")
        current_app.logger.info(f"Registro rechazado (usuario ya existe): {email}")
        return redirect(url_for("auth.register"))

    user_datastore.create_user(
        name=name,
        email=email,
        password=hash_password(password)
    )

    current_app.logger.info(f"Usuario nuevo creado: {email}")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al registrar usuario: {str(e)}")
        flash("Error al crear la cuenta. Intenta de nuevo.", "error")
        return redirect(url_for("auth.register"))

    flash("Cuenta creada exitosamente. Inicia sesión.", "success")
    return redirect(url_for("auth.login"))


# ─────────────────────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────────────────────
@auth.route("/logout")
@login_required
def logout():
    current_user.session_token      = None
    current_user.session_expiration = None

    db.session.commit()

    session.clear()
    logout_user()

    return redirect(url_for("auth.login"))