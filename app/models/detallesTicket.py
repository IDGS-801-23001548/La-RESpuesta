from app.extensions import db

class DetalleTicket(db.Model):
    __tablename__='detallesTicket'
    idDetalle=db.Column(db.Integer, primary_key=True)
    idTicket=db.Column(db.Integer, db.ForeignKey('ticket.idTicket'), nullable=False)
    idProducto=db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False)
    cantidad=db.Column(db.Float, nullable=False)
    subtotal=db.Column(db.Float, nullable=False)