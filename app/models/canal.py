from app.extensions import db


class Canal(db.Model):

    __tablename__ = 'canal'

    idCanal           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMateriaProveida = db.Column(db.Integer, db.ForeignKey('materia_proveida.idMateriaProveida'), nullable=False)
    idCategoria       = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'), nullable=True)
    numeroLote        = db.Column(db.String(20), nullable=True)
    peso              = db.Column(db.Float, nullable=True)   # kg por canal
    fechaSacrificio   = db.Column(db.Date, nullable=True)
    estatus           = db.Column(
        db.Enum('EnEspera', 'Disponible', 'Procesado', 'Cancelado'),
        nullable=False,
        default='EnEspera'
    )

    # Relaciones
    materiaProveida = db.relationship(
        'MateriaProveida',
        backref=db.backref('canales', lazy='dynamic')
    )
    categoria = db.relationship(
        'Categoria',
        backref=db.backref('canales', lazy='dynamic')
    )
