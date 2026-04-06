from app.extensions import db
from datetime import datetime

class Pedido(db.Model):

    __tablename__    = 'pedido'
    idPedido         = db.Column(db.Integer, primary_key=True)
    idUsuario        = db.Column(db.Integer, db.ForeignKey('user.id'))
    Total            = db.Column(db.Float)
    Tipo             = db.Column(db.String(50),  nullable=True)    # Tarjeta | Transferencia | Efectivo
    Estatus          = db.Column(db.String(50),  nullable=True)    # EnCurso | Finalizado | Cancelado
    Entrega          = db.Column(db.String(50),  nullable=True)    # Domicilio | Mostrador
    Direccion        = db.Column(db.String(500), nullable=True)    # Dirección exclusiva de este pedido
    Notas            = db.Column(db.String(500), nullable=True)    # Notas/instrucciones del cliente
    fechaCreacion    = db.Column(db.DateTime, default=datetime.now, nullable=False)

    unidadesPedido   = db.relationship(
        'ProductoUnitario',
        backref='pedido',
        lazy='dynamic'
    )
