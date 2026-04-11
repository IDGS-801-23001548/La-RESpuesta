from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()

mail = Mail()
mongo_client = None
mongo_fotos  = None

db = SQLAlchemy()

# Sin app=current_app — se inicializa después con init_app
limiter = Limiter(get_remote_address)

def limit_by_email():
    return request.form.get("email") or request.remote_addr

def _init_mongo(app):
    global mongo_client, mongo_fotos
    uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/')
    try:
        mongo_client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        mongo_client.server_info()  # fuerza conexión real al arranque
        db_mongo    = mongo_client['La_Respuesta']
        mongo_fotos = db_mongo['La_Respuesta_fotos']
        app.logger.info("MongoDB conectado correctamente")
    except Exception as e:
        app.logger.error(f"MongoDB ERROR: {e}")