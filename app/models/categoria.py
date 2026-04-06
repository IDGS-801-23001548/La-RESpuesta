from app.extensions import db

class Categoria(db.Model):

    __tablename__   = 'categoria'
    idCategoria     = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String(25), nullable=False, unique=True)

    materiasPrimas  = db.relationship(
        'MateriaPrima',
        backref='categoria',
        lazy='dynamic'
    )

    productos       = db.relationship(
        'Producto',
        backref='categoria',
        lazy='dynamic'
    )
