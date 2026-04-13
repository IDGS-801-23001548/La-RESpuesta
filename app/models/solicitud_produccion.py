from app.extensions import db
from datetime import datetime


ESTATUS_SOLICITUD = ('Pendiente', 'Completada', 'Cancelada')

# Una solicitud puede ser:
#  Personalizada → consume lotes de materia prima y produce un Producto terminado
#  Corte         → consume un canal_corte Disponible y produce un Lote
#                  (el catalogo de "recetas de corte" es la tabla Corte directamente)
TIPO_SOLICITUD    = ('Personalizada', 'Corte')


class SolicitudProduccion(db.Model):

    __tablename__         = 'solicitud_produccion'

    idSolicitud           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipoReceta            = db.Column(db.String(20), nullable=False, default='Personalizada')

    # Tipo Personalizada → apunta a una Receta (que produce un Producto)
    idReceta              = db.Column(db.Integer, db.ForeignKey('receta.idReceta'), nullable=True)

    # Tipo Corte → apunta directo a la tabla corte (no hay tabla intermedia de recetas)
    idCorte               = db.Column(db.Integer, db.ForeignKey('corte.idCorte'), nullable=True)

    cantidadProducir      = db.Column(db.Integer, nullable=False, default=1)
    fechaSolicitud        = db.Column(db.DateTime, default=datetime.now, nullable=False)
    fechaCompletada       = db.Column(db.DateTime, nullable=True)
    estatus               = db.Column(db.String(20), nullable=False, default='Pendiente')
    idUsuario             = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    notas                 = db.Column(db.String(500), nullable=True)

    receta = db.relationship(
        'Receta',
        backref=db.backref('solicitudes', lazy='dynamic'),
    )
    corte = db.relationship(
        'Corte',
        backref=db.backref('solicitudes', lazy='dynamic'),
    )
    usuario = db.relationship(
        'User',
        backref=db.backref('solicitudesProduccion', lazy='dynamic'),
    )
    detalles = db.relationship(
        'SolicitudProduccionDetalle',
        backref='solicitud',
        lazy='dynamic',
        cascade='all, delete-orphan',
    )

    @property
    def nombreReceta(self):
        """Nombre legible para mostrar sin importar el tipo."""
        if self.tipoReceta == 'Corte' and self.corte:
            cat = self.corte.categoria.nombreCategoria if self.corte.categoria else None
            return f'{self.corte.nombreCorte} ({cat})' if cat else self.corte.nombreCorte
        if self.receta:
            return self.receta.nombreReceta
        return '—'


class SolicitudProduccionDetalle(db.Model):

    __tablename__ = 'solicitud_produccion_detalle'

    idDetalle   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idSolicitud = db.Column(
        db.Integer,
        db.ForeignKey('solicitud_produccion.idSolicitud'),
        nullable=False,
    )

    # Materia prima involucrada (para tipo Personalizada)
    idMateriaPrima = db.Column(
        db.Integer,
        db.ForeignKey('materia_prima.idMateriaPrima'),
        nullable=True,
    )

    # Para tipo Personalizada: lote que se descontó
    idLote = db.Column(
        db.Integer,
        db.ForeignKey('lote.idLote'),
        nullable=True,
    )

    # Para tipo Corte: canal_corte consumido + lote producido
    idCanalCorte = db.Column(
        db.Integer,
        db.ForeignKey('canal_corte.idCanalCorte'),
        nullable=True,
    )
    idLoteProducido = db.Column(
        db.Integer,
        db.ForeignKey('lote.idLote'),
        nullable=True,
    )

    cantidadConsumida = db.Column(
        db.Float,
        nullable=False,
        default=0.0,
    )

    # Relaciones — ambas FK apuntan a Lote, hay que desambiguar con foreign_keys
    lote = db.relationship('Lote', foreign_keys=[idLote])
    loteProducido = db.relationship('Lote', foreign_keys=[idLoteProducido])
    canalCorte = db.relationship('CanalCorte')
    materiaPrima = db.relationship('MateriaPrima')
