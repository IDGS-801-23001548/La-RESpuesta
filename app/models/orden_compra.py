from app.extensions import db
from datetime import datetime

class OrdenCompra(db.Model):

    __tablename__ = 'orden_compra'

    idOrdenCompra   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProveedor     = db.Column(db.Integer,db.ForeignKey('proveedor.id'),nullable=False)
    numeroLote      = db.Column(db.String(20), nullable=True, unique=True)
    estatus         = db.Column(db.Enum('EnCurso', 'Recibida', 'Cancelada'),nullable=False,default='EnCurso')
    fechaDeOrden    = db.Column(db.Date, default=datetime.now, nullable=False)
    notas           = db.Column(db.String(500), nullable=True)
    totalOrden      = db.Column(db.Float, nullable=False, default=0.0)
    PagoProveedor   = db.Column(db.String(20),nullable=False,default='Pendiente')
    metodoPago      = db.Column(db.String(20), nullable=True)
    fechaPago       = db.Column(db.DateTime, nullable=True)

    # Trazabilidad
    idUsuario       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    idUsuarioPago   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    proveedor = db.relationship(
        'Proveedor',
        backref=db.backref('ordenesCompra', lazy='dynamic')
    )

    canales = db.relationship(
        'Canal',
        backref='ordenCompra',
        lazy='dynamic'
    )

    usuario = db.relationship(
        'User',
        foreign_keys=[idUsuario],
        backref=db.backref('ordenesCompra', lazy='dynamic'),
    )
    usuarioPago = db.relationship(
        'User',
        foreign_keys=[idUsuarioPago],
        backref=db.backref('pagosProveedores', lazy='dynamic'),
    )
