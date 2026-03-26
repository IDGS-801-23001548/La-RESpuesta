#Importamos el objeto de la base de datos de __init__.py
from app.extensions import db

#Definiendo la tabla relacional
users_roles = db.Table('users_roles',
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('roleId', db.Integer, db.ForeignKey('role.id')))