import os
import logging
from datetime import timedelta

from flask import Flask, session, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv

from .models import User, Role, Categoria
from app.extensions import db, limiter, _init_mongo

load_dotenv()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def create_app():
    app = Flask(__name__)

    # ==============================
    # LOGGING
    # ==============================
    app.logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # ==============================
    # LOGIN MANAGER
    # ==============================
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Inicia sesión primero."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    # ==============================
    # CONFIGURACIÓN FLASK / SECURITY
    # ==============================
    app.config['SECURITY_LOGIN_URL']             = '/login'
    app.config['SECURITY_UNAUTHORIZED_VIEW']     = 'auth.login'
    app.config['PERMANENT_SESSION_LIFETIME']     = timedelta(days=7)
    app.config['SECURITY_MSG_UNAUTHENTICATED']   = ("Inicia sesión primero.", "warning")
    app.config['SECURITY_MSG_UNAUTHORIZED']      = ("No tienes permisos para acceder.", "danger")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']                     = os.getenv('SECRET_KEY')  # ← clave fija desde .env
    app.config['SECURITY_PASSWORD_HASH']         = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT']         = 'thisissecretsalt'

    # ==============================
    # CSRF
    # ==============================
    csrf = CSRFProtect(app)

    # ==============================
    # BASE DE DATOS MySQL
    # ==============================
    db_user     = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host     = os.getenv('DB_HOST')
    db_name     = os.getenv('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    # ==============================
    # MONGODB
    # ==============================
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

    # ==============================
    # EXTENSIONES
    # ==============================
    db.init_app(app)
    limiter.init_app(app)
    migrate = Migrate(app, db)
    security = Security(app, user_datastore)
    _init_mongo(app)

    # ==============================
    # RENOVAR SESIÓN EN CADA REQUEST
    # ==============================
    @app.before_request
    def renovar_sesion():
        session.permanent = True
        # El lifetime real lo controla session_expiration en la BD (10 min o 7 días)

    # ==============================
    # BLUEPRINTS
    # ==============================
    from .modules.auth      import auth
    from .modules.admin     import admin
    from .modules.user      import user
    from .modules.compras   import compras
    from .modules.venta     import venta
    from .modules.logs      import log
    from .modules.proveedor import proveedor
    from .modules.materia   import materia

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(compras)
    app.register_blueprint(venta)
    app.register_blueprint(log)
    app.register_blueprint(proveedor)
    app.register_blueprint(materia)

    # ==============================
    # MANEJO DE ERRORES
    # ==============================
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.route("/")
    def index():
        return render_template("index.html")

    return app