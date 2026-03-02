from flask import render_template, request, redirect, url_for, session, flash
from . import auth_bp
from .forms import LoginForm
from app.models import Usuario
from app.extensions import db

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Usuario.query.filter_by(
            nombre_usuario=form.username.data
        ).first()

        if user and user.check_password(form.password.data):
            session['user_id'] = user.id_usuario
            return redirect(url_for('admin.admin'))
            # AGREAR EL LOG DE INICIO DE SESIÓN

        flash("Credenciales incorrectas")

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))