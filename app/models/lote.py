from app.extensions import db
from datetime import datetime


class Lote(db.Model):

    __tablename__     = 'lote'

    idLote            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idOrdenCompra     = db.Column(
        db.Integer,
        db.ForeignKey('orden_compra.idOrdenCompra'),
        nullable=False
    )
    idMateriaProveida = db.Column(
        db.Integer,
        db.ForeignKey('materia_proveida.idMateriaProveida'),
        nullable=False
    )

    cantidadDeUnidad  = db.Column(db.Integer, nullable=False, default=1)
    cantidadPorUnidad = db.Column(db.Float, nullable=False, default=0.0)
    precioPorUnidad   = db.Column(db.Float, nullable=False, default=0.0)
    totalCosto        = db.Column(db.Float, nullable=False, default=0.0)
    totalMateria      = db.Column(db.Float, nullable=False, default=0.0)

    fechaCaducidad    = db.Column(db.Date, nullable=True)
    estatus           = db.Column(
        db.Enum('Disponible', 'Caducado', 'Agotado', 'EnEspera', 'Cancelado'),
        nullable=False,
        default='Disponible'
    )

    materiaProveida = db.relationship(
        'MateriaProveida',
        backref=db.backref('lotes', lazy='dynamic')
    )

    canalCortes = db.relationship(
        'CanalCorte',
        backref='lote',
        lazy='dynamic'
    )
