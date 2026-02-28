import os
from datetime import timedelta

class Config:
    # A02:2021 - Se recomienda usar variables de entorno para la clave secreta [cite: 116]
    SECRET_KEY = os.environ.get('SECRET_KEY') or "ClaveSecretaGOOOOODNoMeLaRobesPorfa"
    
    # A07:2021 - La sesión deberá tener una duración máxima de 10 minutos 
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    
    # Seguridad de Cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # NOTA: El requerimiento A05 prohíbe usar usuarios como 'ROOT' o 'ADMIN' [cite: 210]
    # Se recomienda crear un usuario específico para la app con permisos limitados [cite: 209]
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/LA_RESPUESTA'