#Importamos el objeto de la base de datos de __init__.py
from app.extensions import db
from .users_roles import users_roles
#Importamos la clase UserMixin de flask_security
from flask_security import UserMixin

class User(db.Model, UserMixin):
  
    __tablename__       = 'user'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(50), nullable=False)
    email               = db.Column(db.String(100), unique=True, nullable=False)
    password            = db.Column(db.String(255), nullable=False)
    fs_uniquifier       = db.Column(db.String(255), unique=True, nullable=False)
    active              = db.Column(db.Boolean)
    confirmed_at        = db.Column(db.DateTime)
    roles               = db.relationship('Role',
                                    secondary=users_roles,
                                    backref= db.backref('user', lazy='dynamic'))
    
    intentos_fallidos   = db.Column(db.Integer, default=0, nullable=False)
    bloqueado_hasta     = db.Column(db.DateTime, nullable=True)

    ultima_sesion       = db.Column(db.DateTime, nullable=True)
    ultima_ip           = db.Column(db.String(45), nullable=True)
    session_token       = db.Column(db.String(255), nullable=True)
    session_expiration  = db.Column(db.DateTime, nullable=True)
    
    persona             = db.relationship('Persona', 
                                    backref='user', 
                                    uselist=False)
    
    pedido              = db.relationship('Pedido', 
                                    backref='userPedido')