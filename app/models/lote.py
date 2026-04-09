from app.extensions import db
from datetime import datetime


class Lote(db.Model):

    __tablename__   = 'lote'

    idLote          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numeroLote      = db.Column(db.String(25), nullable=False, unique=True)
    Stock           = db.Column(db.Float, nullable=True)
    fechaCaducidad  = db.Column(db.Date, nullable=True)
    estatus         = db.Column(
        db.Enum('Disponible', 'Caducado', 'Agotado'),
        nullable=False,
        default='Disponible'
    )

    canalCortes = db.relationship(
        'CanalCorte',
        backref='lote',
        lazy='dynamic'
    )
