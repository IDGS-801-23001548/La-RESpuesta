from app.extensions import db

class ProductoUnitario(db.Model):

    __tablename__               = 'producto_unitario'
    idProductoUnitario          = db.Column(db.Integer, primary_key=True) #su id
    idProducto                  = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False) #Tipo especifico de producto al que pertenece
    idPedido                    = db.Column(db.Integer, db.ForeignKey('pedido.idPedido')) #Relacion con el pedido Online/Mostrador
    NumeroLote                  = db.Column(db.String(100), nullable=False) #Lote de donde viene este producto en concreto
    FechaCaducidad              = db.Column(db.Date, nullable=True) 
    estatus                     = db.Column(db.String(100), nullable=False) #Vendido, Caducado, Disponible, Desechado, etc