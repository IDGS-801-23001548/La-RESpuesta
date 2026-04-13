from app.extensions import db

class Ticket(db.Model):
    __tablename__='ticket'
    idTicket=db.Column(db.Integer, primary_key=True)
    folioTicket=db.Column(db.String(50), nullable=False)
    fechaCompra=db.Column(db.DateTime, nullable=False)
    totalCompra=db.Column(db.Float, nullable=False)

    detalles = db.relationship('DetalleTicket', backref='ticket', lazy=True)
