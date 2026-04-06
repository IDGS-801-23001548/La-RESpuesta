from app.extensions import db
from datetime import datetime

class OrdenCompra(db.Model):

    __tablename__       = 'orden_compra'
    idOrdenCompra       = db.Column(db.Integer, primary_key=True)
    idMateriaProveida   = db.Column(db.Integer, db.ForeignKey('materia_proveida.idMateriaProveida'), nullable=False)
    cantidadPorUnidad   = db.Column(db.Float, nullable=True)     # Ej: 5 kilos por paquete
    cantidadDeUnidad    = db.Column(db.Integer, nullable=True)   # Ej: 5 paquetes
    precioPorUnidad     = db.Column(db.Float, nullable=True)     # Ej: 10 pesos
    totalCosto          = db.Column(db.Float, nullable=True)     # Ej: 50 pesos
    totalMateria        = db.Column(db.Float, nullable=True)     # Ej: 25 kilogramos
    numeroLote          = db.Column(db.String(10), nullable=True)
    estatus             = db.Column(db.String(20), nullable=True)  # EnCurso | Finalizado | Cancelado
    fechaDeOrden        = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    notas               = db.Column(db.String(500), nullable=True)
