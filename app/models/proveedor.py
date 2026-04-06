from app.extensions import db
from datetime import datetime


class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre         = db.Column(db.String(150), nullable=False)
    rfc            = db.Column(db.String(13),  nullable=False, unique=True)
    estatus        = db.Column(
                        db.Enum('activo', 'inactivo'),
                        nullable=False,
                        default='activo'
                     )
    contacto       = db.Column(db.String(100), nullable=False)
    telefono       = db.Column(db.String(20),  nullable=False)
    correo         = db.Column(db.String(120), nullable=True)
    direccion      = db.Column(db.String(250), nullable=True)

    condicion_pago = db.Column(
                        db.Enum('contado', 'credito_8', 'credito_15', 'credito_30'),
                        nullable=False
                     )

    dias_entrega   = db.Column(db.String(100), nullable=True)
    notas          = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)

    materiasProveidas = db.relationship(
        'MateriaProveida',
        backref='proveedor',
        lazy='dynamic'
    )

    # ------------------------------------------------------------------
    # Propiedades de conveniencia (no columnas extra)
    # ------------------------------------------------------------------

    @property
    def dias_entrega_lista(self):
        """Devuelve los dias de entrega como lista Python."""
        return self.dias_entrega.split(',') if self.dias_entrega else []

    @property
    def dias_credito(self):
        """Dias de plazo de pago derivados de condicion_pago (0 = contado).
        Usar en la ruta de compras para calcular la fecha de vencimiento:
            fecha_vencimiento = fecha_compra + timedelta(days=proveedor.dias_credito)
        """
        _mapa = {'contado': 0, 'credito_8': 8, 'credito_15': 15, 'credito_30': 30}
        return _mapa.get(self.condicion_pago, 0)

    @property
    def es_activo(self):
        return self.estatus == 'activo'
