from app.extensions import db

class Producto(db.Model):

    __tablename__               = 'producto'
    idProducto                  = db.Column(db.Integer, primary_key=True)
    idFoto                      = db.Column(db.String(255), nullable=True)
    NombreProducto              = db.Column(db.String(100), nullable=False)
    DescripcionProducto         = db.Column(db.String(500), nullable=True)
    PrecioCompraProducto        = db.Column(db.Float, nullable=False)
    PrecioVentaProducto         = db.Column(db.Float, nullable=False)
    StockProducto               = db.Column(db.Integer, default=0, nullable=False)

    unidades                    = db.relationship('ProductoUnitario',
                                        backref='producto',
                                        lazy='dynamic')