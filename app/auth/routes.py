from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required
from flask_security.utils import login_user, logout_user
from app.models import User
from app.extensions import db
from app import user_datastore
from flask_security.utils import verify_password, hash_password
from . import auth

@auth.route("/login",)
def login():
    return render_template("security/login_user.html")

@auth.route("/login", methods = ['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    #Consultamos si existe el ususario con la base de datos
    user = User.query.filter_by(email=email).first()
    
    #Verificamos si existe el ususario
    if not user or not verify_password(password, user.password):
        flash("El usuario y/o la contraseña son incorrecto")
        #Log de inicio de sesión fallido
        current_app.logger.warning(f"Intento fallido de login: {email}")
        return redirect(url_for("auth.login"))
    
    #Creamos una sesion y logueamos al usuario
    login_user(user, remember=remember)
    session.permanent = True

    #Log de inicio de sesión exitoso
    current_app.logger.info(f"Loggin exitoso: {email}")
    
    if user.has_role('admin'):
        return redirect(url_for('admin.dashboard'))
    
    elif user.has_role('end-user'):
        return redirect(url_for('main.user_dashboard'))
    
    # fallback por seguridad
    return redirect(url_for("main.profile"))

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
def logout():
    #Cerramos sesión
    logout_user()
    return redirect(url_for("admin.index"))