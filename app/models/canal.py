from app.extensions import db

class Canal(db.Model):

    __tablename__ = 'canal'

    idCanal = db.Column(db.Integer, primary_key=True, autoincrement=True)

    idMateriaProveida = db.Column(
        db.Integer,
        db.ForeignKey('materia_proveida.idMateriaProveida'),
        nullable=False
    )

    idCategoria = db.Column(
        db.Integer,
        db.ForeignKey('categoria.idCategoria'),
        nullable=False
    )

    idOrdenCompra = db.Column( 
        db.Integer,
        db.ForeignKey('orden_compra.idOrdenCompra'),
        nullable=False
    )

    descripcion = db.Column(db.String(200), nullable=True)

    peso = db.Column(db.Float, nullable=True)

    fechaSacrificio = db.Column(db.Date, nullable=True) 

    estatus = db.Column(
        db.Enum('Disponible', 'EnEspera', 'Cancelado'),
        nullable=False,
        default='EnEspera'
    )

    categoria = db.relationship(
        'Categoria',
        backref=db.backref('canales', lazy='dynamic')
    )

    canalCortes = db.relationship(
        'CanalCorte',
        backref='canal',
        lazy='dynamic'
    )