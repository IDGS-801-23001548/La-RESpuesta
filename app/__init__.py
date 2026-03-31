#Archivo de configuración que tiene la función de crear nuestra aplicación, iniciar la base de datos y registrará nuestros modelos
#Importamos el módulo os
import os
#Importamos la clase Flask del módulo flask
from flask import Flask, session, render_template, current_app
#Importamos la clase Security y SQLAlchemyUserDatastore de flask-security
from flask_security import Security, SQLAlchemyUserDatastore
#Importamos la función generate_password_hash de werkzeug.security
from flask_security.utils import hash_password
#Importamos la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager
from dotenv import load_dotenv
from datetime import timedelta
import os
from .models import User, Role
from app.extensions import db
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
load_dotenv()

#Creamos el objeto SQLAlchemyUserDatastore con base a los modelos User y Role.
from .models import User, Role
  
#Método de inicio de la aplicación
def create_app():
    #Creamos una instancia de Flask
    app = Flask(__name__)
    migrate = Migrate(app, db)
    # Nivel mínimo de logs (DEBUG, INFO, WARNING, ERROR)
    app.logger.setLevel(logging.DEBUG)

    #Guardar los logs en el archivo app.log
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Inicia sesión primero."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    #Definimos a donde redirigir cuando no hay sesión y el tiempo de vida de la sesión
    app.config['SECURITY_LOGIN_URL'] = '/login'
    app.config['SECURITY_UNAUTHORIZED_VIEW'] = 'auth.login'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

    #Configuramos los mensajes de errores controlados
    app.config['SECURITY_MSG_UNAUTHENTICATED'] = ("Inicia sesión primero.", "warning")
    app.config['SECURITY_MSG_UNAUTHORIZED'] = ("No tienes permisos para acceder.", "danger")
 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generamos la clave aleatoria de sesión Flask para crear una cookie con la inf. de la sesión
    app.config['SECRET_KEY'] = os.urandom(24)
    csrf = CSRFProtect(app)
    #Definimos la ruta a la BD: mysql://user:password@localhost/bd'
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    )
    # We're using PBKDF2 with salt.
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'
 
    #Conectando los modelos a fask-security usando SQLAlchemyUserDatastore
    security = Security(app, user_datastore)
   
    #Inicializamos y creamos la BD
    db.init_app(app)

    # ==============================
    # BLUEPRINTS
    # ==============================
    from .modules.auth import auth
    from .modules.admin import admin
    from .modules.user import user
    from .modules.compras import compras

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(compras)

    # ==============================
    # ERROR 404
    # ==============================
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app