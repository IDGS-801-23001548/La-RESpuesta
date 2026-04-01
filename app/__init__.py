from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask import g

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.secret_key = 'secret'

    db.init_app(app)
    csrf.init_app(app)

    # Registrar blueprints
    from .auth import auth_bp
    from .admin import admin_bp
<<<<<<< HEAD

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
=======
    from .entregas import entregas_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(entregas_bp)
>>>>>>> develop

    return app