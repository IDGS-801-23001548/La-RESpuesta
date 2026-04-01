from app import create_app
from app.extensions import db
from flask import request
from flask_security.utils import hash_password
from flask import session, redirect, url_for
from flask_login import current_user, logout_user
from app.models import Persona
from app import create_app, user_datastore
from datetime import datetime
from app.models import User

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        #Primer log de la aplicación en ejecución
        app.logger.debug("La aplicación ha iniciado correctamente")

        expired_users = User.query.filter(
            User.session_expiration < datetime.now()
        ).all()

        for user in expired_users:
            user.session_token = None
            user.session_expiration = None

        db.session.commit()
        app.logger.debug("Tokens de sesión eliminados")

        db.create_all()

        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='Gerente', description='Administrador general del sistema')
        user_datastore.find_or_create_role(name='Cajero', description='Cobrador de mostrador')
        user_datastore.find_or_create_role(name='Repartidor', description='Entregas a domicilio')
        user_datastore.find_or_create_role(name='Cliente', description='Ventas en linea')
        user_datastore.find_or_create_role(name='end-user', description='End user')

        encrypted_password = hash_password('password')

        if not user_datastore.find_user(email='admin@example.com'):
            user = user_datastore.create_user(
                name        = 'admin', 
                email       = 'admin@example.com', 
                password    = encrypted_password)
            
            user_datastore.add_role_to_user(user, 'admin')
            
            persona = Persona(
                nombre              ='admin',
                apellido_paterno    ='admin',
                apellido_materno    ='admin',
                telefono            ='9999999999',
                direccion           ='León, Gto',
                user=user
            )

            db.session.add(persona)

        if not user_datastore.find_user(email='emmanuel@example.com'):
            user = user_datastore.create_user(
                name        = 'Emmanuel', 
                email       = 'emmanuel@example.com', 
                password    = encrypted_password)
 
            user_datastore.add_role_to_user(user, 'admin')

            persona = Persona(
                nombre              ='Emmanuel',
                apellido_paterno    ='Ortiz',
                apellido_materno    ='Reyes',
                telefono            ='4773845271',
                direccion           ='León, Gto',
                user                =user
            )
            db.session.add(persona)

        db.session.commit()

        user = user_datastore.find_user(email='emmanuel@example.com')
        if user:
            user_datastore.add_role_to_user(user, 'admin')

    @app.before_request
    def before_request():
        session.permanent = True

        rutas_excluidas = [
        "auth.login",
        "auth.login_post",
        "static"
        ]
        
        if request.endpoint in rutas_excluidas:
            return
        
        if current_user.is_authenticated:
            token_db = current_user.session_token
            token_session = session.get("session_token")
            expiration = current_user.session_expiration

            if not token_db or not token_session or token_db != token_session or not expiration or expiration < datetime.now():
                app.logger.warning(
                    f"Sesión inválida | user={current_user.id}"
                )
                current_user.session_token = None
                current_user.session_expiration = None
                logout_user()
                session.clear()
                return redirect(url_for("auth.login"))

    app.run(debug=True)