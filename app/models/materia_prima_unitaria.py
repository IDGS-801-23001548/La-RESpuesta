from app.extensions import db


# Valores válidos de estatus — se usan en back para validar y en front para mostrar
ESTATUS_MPU = ('EnEspera', 'Disponible', 'Agotado', 'Caducado', 'Cancelado')


class MateriaPrimaUnitaria(db.Model):

    __tablename__              = 'materia_prima_unitaria'
    idMateriaPrimaUnitaria     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMateriaProveida          = db.Column(db.Integer, db.ForeignKey('materia_proveida.idMateriaProveida'), nullable=False)
    idOrdenCompra              = db.Column(db.Integer, db.ForeignKey('orden_compra.idOrdenCompra'), nullable=False)

    # Cuántas unidades de compra (ej: 5 cajas)
    cantidadDeUnidad           = db.Column(db.Float, nullable=False, default=0.0)
    # Cuántas unidades del conversor hay en una unidad de compra (ej: 60 piezas por caja)
    cantidadPorUnidad          = db.Column(db.Float, nullable=False, default=0.0)
    # Precio de una unidad de compra (ej: $250 por caja)
    precioPorUnidad            = db.Column(db.Float, nullable=False, default=0.0)
    # Total en cantidad del conversor (ej: 300 piezas)
    totalMateria               = db.Column(db.Float, nullable=False, default=0.0)
    # Total en dinero (ej: $1250)
    totalCosto                 = db.Column(db.Float, nullable=False, default=0.0)

    # EnEspera  → orden EnCurso (aún no llega)
    # Disponible → orden Recibida (ya está en inventario)
    # Agotado / Caducado / Cancelado → manejados desde módulo de recetas / producción
    estatus                    = db.Column(db.String(20), nullable=False, default='EnEspera')

    # Relación hacia MateriaProveida
    materiaProveida            = db.relationship(
        'MateriaProveida',
        backref=db.backref('materiasPrimasUnitarias', lazy='dynamic')
    )

    # Relación hacia OrdenCompra
    ordenCompra                = db.relationship(
        'OrdenCompra',
        backref=db.backref('materiasPrimasUnitarias', lazy='dynamic')
    )
