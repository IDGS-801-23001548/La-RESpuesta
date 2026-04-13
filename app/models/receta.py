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
    """Ingrediente de una receta.

    Cada fila representa UN ingrediente que puede ser:
      - Materia prima  → idMateriaPrima != NULL, idCorte = NULL
      - Corte          → idCorte != NULL, idMateriaPrima = NULL

    Al menos uno de los dos FK debe estar presente.
    """

    __tablename__              = 'receta_materia_prima'
    idRecetaMateriaPrima       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta                   = db.Column(db.Integer, db.ForeignKey('receta.idReceta'), nullable=False)

    # FK a materia prima (ingrediente tipo materia)
    idMateriaPrima             = db.Column(db.Integer, db.ForeignKey('materia_prima.idMateriaPrima'), nullable=True)

    # FK a corte (ingrediente tipo corte)
    idCorte                    = db.Column(db.Integer, db.ForeignKey('corte.idCorte'), nullable=True)

    cantidadUsada              = db.Column(db.Float, nullable=False, default=0.0)

    materiaPrima               = db.relationship(
        'MateriaPrima',
        backref=db.backref('usosEnRecetas', lazy='dynamic')
    )
    corte                      = db.relationship(
        'Corte',
        backref=db.backref('usosEnRecetas', lazy='dynamic')
    )

    @property
    def tipo_ingrediente(self):
        """Devuelve 'materia' o 'corte' segun el FK que este poblado."""
        if self.idCorte:
            return 'corte'
        return 'materia'

    @property
    def nombre_ingrediente(self):
        """Nombre legible del ingrediente."""
        if self.idCorte and self.corte:
            cat = self.corte.categoria
            return f"{self.corte.nombreCorte} ({cat.nombreCategoria})" if cat else self.corte.nombreCorte
        if self.idMateriaPrima and self.materiaPrima:
            return self.materiaPrima.nombreMateriaPrima
        return '—'
