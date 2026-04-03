from app.extensions import db
from datetime import datetime

class Pedido(db.Model):

    __tablename__    = 'pedido'
    idPedido         = db.Column(db.Integer, primary_key=True)
    idUsuario        = db.Column(db.Integer, db.ForeignKey('user.id'))
    Total            = db.Column(db.Float)
    Tipo             = db.Column(db.String(50), nullable=True)   # método de pago
    Estatus          = db.Column(db.String(50), nullable=True)   # EnCurso | Finalizado | Cancelado
    Entrega          = db.Column(db.String(50), nullable=True)   # Domicilio | Mostrador
    fechaCreacion    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    unidadesPedido   = db.relationship(
        'ProductoUnitario',
        backref='pedido',
        lazy='dynamic'
    )
