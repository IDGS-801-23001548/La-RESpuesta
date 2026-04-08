from app.extensions import db


# Tipos validos de receta. Por ahora solo se trabaja con MateriaPrima.
# Canal se incorporara mas adelante.
TIPOS_RECETA = ('MateriaPrima', 'Canal')


class Receta(db.Model):

    __tablename__   = 'receta'
    idReceta        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreReceta    = db.Column(db.String(100), nullable=False, unique=True)
    idProducto      = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False)
    idFoto          = db.Column(db.String(255), nullable=True)
    descripcion     = db.Column(db.String(500), nullable=True)
    tipo            = db.Column(db.String(20), nullable=False, default='MateriaPrima')

    producto        = db.relationship(
        'Producto',
        backref=db.backref('recetas', lazy='dynamic')
    )

    materiasPrimas  = db.relationship(
        'RecetaMateriaPrima',
        backref='receta',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


class RecetaMateriaPrima(db.Model):

    __tablename__              = 'receta_materia_prima'
    idRecetaMateriaPrima       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta                   = db.Column(db.Integer, db.ForeignKey('receta.idReceta'), nullable=False)
    idMateriaPrima             = db.Column(db.Integer, db.ForeignKey('materia_prima.idMateriaPrima'), nullable=False)
    cantidadUsada              = db.Column(db.Float, nullable=False, default=0.0)

    materiaPrima               = db.relationship(
        'MateriaPrima',
        backref=db.backref('usosEnRecetas', lazy='dynamic')
    )
