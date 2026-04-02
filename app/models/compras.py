from app.extensions import db
from datetime import datetime


class OrdenCompra(db.Model):
    __tablename__ = 'ordenes_compra'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Folio legible: OC-0001, OC-0002, ...
    folio             = db.Column(db.String(20), unique=True, nullable=False)

    proveedor_id      = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)

    # Fecha en que se registra la compra
    fecha             = db.Column(db.Date, nullable=False)
    # Fecha estimada de entrega del proveedor
    fecha_entrega     = db.Column(db.Date, nullable=True)
    # Calculada al crear: fecha + proveedor.dias_credito
    fecha_vencimiento = db.Column(db.Date, nullable=True)

    estado            = db.Column(
                            db.Enum('pendiente', 'recibida', 'cancelada'),
                            nullable=False,
                            default='pendiente'
                        )

    notas             = db.Column(db.Text, nullable=True)

    # Total almacenado para evitar recalcular en listados
    total             = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    fecha_registro    = db.Column(db.DateTime, default=datetime.now)

    # ── Relaciones ──────────────────────────────────────────────────────
    proveedor = db.relationship('Proveedor', backref='ordenes_compra')
    detalles  = db.relationship(
        'DetalleCompra',
        backref='orden',
        lazy=True,
        cascade='all, delete-orphan'
    )

    @property
    def num_productos(self):
        """Número de líneas distintas en la orden."""
        return len(self.detalles)


class DetalleCompra(db.Model):
    __tablename__ = 'detalles_compra'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orden_id          = db.Column(db.Integer, db.ForeignKey('ordenes_compra.id'), nullable=False)
    materia_id        = db.Column(db.Integer, db.ForeignKey('materias_primas.id_materia'), nullable=False)

    # Cantidad comprada en la unidad de compra (ej. 2 canales, 50 kg)
    cantidad          = db.Column(db.Numeric(12, 4), nullable=False)

    # Unidad en que se compró: kg, g, l, ml, ton, pza
    unidad_compra     = db.Column(db.String(10), nullable=False)

    # Cuántas unidades estándar equivale 1 unidad de compra
    # Ej. 1 canal = 200 000 g  →  factor_conversion = 200000
    factor_conversion = db.Column(db.Numeric(12, 4), nullable=False, default=1)

    # Unidad estándar destino: g | ml | pza
    unidad_estandar   = db.Column(db.Enum('g', 'ml', 'pza'), nullable=False, default='g')

    # Costo por 1 unidad de compra (no por unidad estándar)
    costo_unitario    = db.Column(db.Numeric(10, 4), nullable=False)

    # cantidad * costo_unitario
    subtotal          = db.Column(db.Numeric(12, 2), nullable=False)

    # ── Relación ────────────────────────────────────────────────────────
    materia_prima = db.relationship('MateriaPrima', backref='detalles_compra')

    # ── Propiedades ─────────────────────────────────────────────────────

    @property
    def cantidad_en_estandar(self):
        """Cantidad convertida a la unidad estándar.
        Usar al actualizar stock al recibir la orden:
            materia.stock_actual += detalle.cantidad_en_estandar
        """
        return float(self.cantidad) * float(self.factor_conversion)

    @property
    def costo_por_estandar(self):
        """Costo por unidad estándar.
        Usar para recalcular costo_promedio ponderado en MateriaPrima:
            costo_promedio = (stock_prev * costo_prev + cant_std * det.costo_por_estandar)
                           / nuevo_stock
        """
        if float(self.factor_conversion) == 0:
            return 0
        return float(self.costo_unitario) / float(self.factor_conversion)
