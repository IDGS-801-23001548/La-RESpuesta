from app.extensions import db
from datetime import datetime

class Carrito(db.Model):

    __tablename__ = 'carrito'

    idCarrito = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    fechaCreacion = db.Column(db.DateTime, default=datetime.now)

    productos = db.relationship(
        'ProductoUnitario',
        backref='carrito',
        lazy='dynamic'
    )