from app.extensions import db

class MateriaPrima(db.Model):

    __tablename__       = 'materia_prima'
    idMateriaPrima      = db.Column(db.Integer, primary_key=True)
    nombreMateriaPrima  = db.Column(db.String(25), nullable=False)
    idCategoria         = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'), nullable=True)
    tipo                = db.Column(db.String(25), nullable=True)
    idProducto          = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=True)

    materiasProveidas   = db.relationship(
        'MateriaProveida',
        backref='materiaPrima',
        lazy='dynamic'
    )
