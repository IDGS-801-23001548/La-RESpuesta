from app.extensions import db
from datetime import datetime

class MateriaPrima(db.Model):
    __tablename__   = 'materias_primas'

    id_materia      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre          = db.Column(db.String(100), nullable=False)
    descripcion     = db.Column(db.Text, nullable=True)

    # Canal | Insumo | Reventa
    categoria       = db.Column(
                        db.Enum('Canal', 'Insumo', 'Reventa'),
                        nullable=False
                      )

    # Unidad en la que se COMPRA (canal, pieza, bulto, kg, litro...)
    unidad_compra   = db.Column(db.String(30), nullable=False)

    # Unidad en la que se ALMACENA en inventario (g, ml, pza)
    unidad_estandar = db.Column(db.Enum('g', 'ml', 'pza'), nullable=False, default='g')

    # Cuántas unidades estándar equivale 1 unidad de compra
    # Ej. 1 canal = 200000 g  →  factor_conversion = 200000
    factor_conversion = db.Column(db.Numeric(12, 4), nullable=True)

    # Tipo de merma como cadena separada por comas (solo Canal e Insumo)
    # Valores posibles: produccion, manejo, desperdicio
    tipo_merma      = db.Column(db.String(100), nullable=True)

    # % de merma (solo Canal e Insumo)
    pct_merma       = db.Column(db.Numeric(5, 2), nullable=True, default=0)

    # Stock mínimo en unidad estándar para alertas
    stock_minimo    = db.Column(db.Numeric(12, 4), nullable=False, default=0)

    # Stock actual en unidad estándar (se actualiza con compras y producción)
    stock_actual    = db.Column(db.Numeric(12, 4), nullable=False, default=0)

    # Costo promedio por unidad estándar (se recalcula con cada compra)
    costo_promedio  = db.Column(db.Numeric(10, 4), nullable=True, default=0)

    activo          = db.Column(db.Boolean, default=True)
    fecha_registro  = db.Column(db.DateTime, default=datetime.now)

    # Relación con detalle de compras (se usará en el módulo de compras)
    # compras = db.relationship('DetalleCompra', backref='materia_prima', lazy=True)

    @property
    def tipo_merma_lista(self):
        if self.tipo_merma:
            return self.tipo_merma.split(',')
        return []

    def stock_en_kg(self):
        if self.unidad_estandar == 'g' and self.stock_actual:
            return float(self.stock_actual) / 1000
        return float(self.stock_actual or 0)

    @property
    def esta_bajo_minimo(self):
        return float(self.stock_actual or 0) < float(self.stock_minimo or 0)

    @property
    def esta_critico(self):
        return float(self.stock_actual or 0) < float(self.stock_minimo or 0) * 0.5