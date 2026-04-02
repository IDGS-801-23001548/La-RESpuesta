from app.extensions import db

class ProductoUnitario(db.Model):

    __tablename__               = 'producto_unitario'
    idProductoUnitario          = db.Column(db.Integer, primary_key=True)
    idProducto                  = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False)
    NumeroLote                  = db.Column(db.String(100), nullable=False)
    FechaCaducidad              = db.Column(db.Date, nullable=True)