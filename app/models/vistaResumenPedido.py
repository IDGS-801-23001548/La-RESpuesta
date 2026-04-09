from app.extensions import db

class VistaResumenPedido(db.Model):
    __tablename__ = 'vista_resumen_pedido'

    # Las vistas no tienen PK real, declaramos una compuesta
    idPedido             = db.Column(db.Integer, primary_key=True)
    idProducto           = db.Column(db.Integer, primary_key=True)
    NombreProducto       = db.Column(db.String(255))
    PrecioVentaProducto  = db.Column(db.Float)
    cantidad             = db.Column(db.Integer)
    subtotal             = db.Column(db.Float)