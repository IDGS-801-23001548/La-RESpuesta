from flask import request, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import current_user
from flask_security.utils import login_user, logout_user, verify_password, hash_password
from app.models import User
from app.extensions import db, limiter, limit_by_email
from app import user_datastore
from flask_security import login_required
from . import auth
from datetime import datetime, timedelta
import uuid

@auth.route("/login",)
def login():
    return render_template("security/login_user.html")

@auth.route("/login", methods=['POST'])
@limiter.limit("5 per minute")
@limiter.limit("3 per minute", key_func=limit_by_email)
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(email=email).first()

    if user and user.bloqueado_hasta:
        if datetime.now() < user.bloqueado_hasta:
            current_app.logger.warning(
                f"Intento en cuenta bloqueada | email={email} | ip={request.remote_addr}"
            )
            flash("Cuenta bloqueada temporalmente. Intenta más tarde.")
            return redirect(url_for("auth.login"))

    is_valid = user and verify_password(password, user.password)

    if not is_valid:
        
        if user:
            user.intentos_fallidos = (user.intentos_fallidos or 0) + 1

            if user.intentos_fallidos >= 5 and not user.bloqueado_hasta:
                user.bloqueado_hasta = datetime.now() + timedelta(minutes=10)
                user.active = 0

                current_app.logger.warning(
                    f"Usuario bloqueado por intentos | email={email}"
                )

            db.session.commit()

        current_app.logger.warning(
            f"Intento fallido | email={email} | ip={request.remote_addr}"
        )

        flash("El usuario y/o la contraseña son incorrectos")
        return redirect(url_for("auth.login"))
    
    #Logs de auditoria en la base de datos
    user.session_token = str(uuid.uuid4())
    if remember:
        user.session_expiration = datetime.now() + timedelta(days=7)
    else:
        user.session_expiration = datetime.now() + timedelta(minutes=10) 
    user.ultima_sesion = datetime.now()
    user.ultima_ip = request.remote_addr

    session["session_token"] = user.session_token

    #Reset de seguridad
    user.intentos_fallidos = 0
    user.bloqueado_hasta = None

    db.session.commit()

    login_user(user, remember=remember)
    session.permanent = True

    current_app.logger.info(
        f"Login exitoso | email={email} | ip={request.remote_addr}"
    )
    
    if user.has_role('admin'):
        return redirect(url_for('admin.dashboard'))
    
    elif user.has_role('Cajero'):
        return redirect(url_for('mostrador.mostradorVenta'))
    
    elif user.has_role('end-user'):
        return f"Bienvenido {email}"
    
    return f"Bienvenido {email}"

@auth.route("/register")
def register():
    return render_template("security/register.html")

@auth.route("/register", methods = ['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    #Consultamos si existe un usuario con este email
    user = User.query.filter_by(email=email).first()
    
    if user:
        flash("Ya existe un usuario con este email")
        current_app.logger.info(f"Registro rechazado (usuario ya existe): {email}")
        return redirect(url_for("auth.register"))
    
    #Creamos un nuevo usuario
    user_datastore.create_user(
        name=name, 
        email=email, 
        password=hash_password(password)    
        )
    
    #Log de inicio de sesión fallido
    current_app.logger.info(f"Usuario nuevo creado: {email}")
    
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error al registrar usuario: {str(e)}")
    
    return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    current_user.session_token = None
    current_user.session_expiration = None
    db.session.commit()

    logout_user()
    session.clear()

    return redirect(url_for("auth.login"))