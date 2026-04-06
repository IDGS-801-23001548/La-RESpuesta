from app.extensions import db
from datetime import datetime


class OrdenCompra(db.Model):

    __tablename__   = 'orden_compra'

    idOrdenCompra   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProveedor     = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    numeroLote      = db.Column(db.String(20), nullable=True, unique=True)
    estatus         = db.Column(
        db.Enum('EnCurso', 'Recibida', 'Cancelada'),
        nullable=False,
        default='EnCurso'
    )
    fechaDeOrden    = db.Column(db.Date, default=datetime.now, nullable=False)
    notas           = db.Column(db.String(500), nullable=True)
    totalOrden      = db.Column(db.Float, nullable=False, default=0.0)

    proveedor = db.relationship(
        'Proveedor',
        backref=db.backref('ordenesCompra', lazy='dynamic')
    )
