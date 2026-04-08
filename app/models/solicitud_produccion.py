from app.extensions import db
from datetime import datetime


ESTATUS_SOLICITUD = ('Pendiente', 'Completada', 'Cancelada')


class SolicitudProduccion(db.Model):

    __tablename__         = 'solicitud_produccion'
    idSolicitud           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta              = db.Column(db.Integer, db.ForeignKey('receta.idReceta'), nullable=False)
    cantidadProducir      = db.Column(db.Integer, nullable=False, default=1)
    fechaSolicitud        = db.Column(db.DateTime, default=datetime.now, nullable=False)
    fechaCompletada       = db.Column(db.DateTime, nullable=True)
    estatus               = db.Column(db.String(20), nullable=False, default='Pendiente')
    idUsuario             = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    notas                 = db.Column(db.String(500), nullable=True)

    receta                = db.relationship(
        'Receta',
        backref=db.backref('solicitudes', lazy='dynamic')
    )

    usuario               = db.relationship(
        'User',
        backref=db.backref('solicitudesProduccion', lazy='dynamic')
    )

    detalles              = db.relationship(
        'SolicitudProduccionDetalle',
        backref='solicitud',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


class SolicitudProduccionDetalle(db.Model):

    __tablename__ = 'solicitud_produccion_detalle'

    idDetalle   = db.Column(db.Integer, primary_key=True, autoincrement=True)

    idSolicitud = db.Column(
        db.Integer,
        db.ForeignKey('solicitud_produccion.idSolicitud'),
        nullable=False
    )

    idLote = db.Column(
        db.Integer,
        db.ForeignKey('lote.idLote'),
        nullable=False
    )

    cantidadConsumida = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    # Relaciones correctas
    lote = db.relationship('Lote')
