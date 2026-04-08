from app.extensions import db
from datetime import datetime


class Retiro(db.Model):
    """Salida manual de dinero (efectivo o transferencia bancaria)."""
    __tablename__ = 'retiro'

    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    tipo    = db.Column(db.String(20), nullable=False, default='Retiro')  # 'Ingreso' | 'Retiro'
    origen  = db.Column(db.String(20), nullable=False)                     # 'Efectivo' | 'Transferencia'
    monto   = db.Column(db.Float, nullable=False)
    motivo  = db.Column(db.String(255), nullable=True)
    usuario = db.Column(db.String(120), nullable=True)
