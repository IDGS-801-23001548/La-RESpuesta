from app.extensions import db


class Lote(db.Model):
    """
    Lote unifica dos fuentes de inventario:

    1) Produccion — generado al procesar un canal_corte dentro de una
       solicitud de produccion tipo Corte. Se llena idCanalCorte; los
       campos idMateriaProveida / idOrdenCompra quedan null.

    2) Compra directa de materia prima (tipo Materia) — el lote representa
       la entrada directa al inventario desde una orden de compra.
       Se llenan idMateriaProveida + idOrdenCompra; idCanalCorte queda null.

    En ambos casos el campo `totalMateria` lleva el stock actual disponible
    del lote (se descuenta al consumirse en recetas personalizadas).
    """

    __tablename__     = 'lote'

    idLote            = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Fuente 1 — lote obtenido por procesar un canal_corte (receta de corte)
    idCanalCorte      = db.Column(
        db.Integer,
        db.ForeignKey('canal_corte.idCanalCorte'),
        nullable=True,
    )

    # Fuente 2 — lote obtenido por compra directa de materia prima
    idMateriaProveida = db.Column(
        db.Integer,
        db.ForeignKey('materia_proveida.idMateriaProveida'),
        nullable=True,
    )
    idOrdenCompra     = db.Column(
        db.Integer,
        db.ForeignKey('orden_compra.idOrdenCompra'),
        nullable=True,
    )

    numeroLote        = db.Column(db.String(25), nullable=False)

    # Cantidades — cubren tanto el desglose de compra como el stock remanente
    cantidadDeUnidad  = db.Column(db.Integer, nullable=True, default=0)
    cantidadPorUnidad = db.Column(db.Float,   nullable=True, default=0.0)
    totalMateria      = db.Column(db.Float,   nullable=True, default=0.0)  # stock actual
    precioPorUnidad   = db.Column(db.Float,   nullable=True, default=0.0)
    totalCosto        = db.Column(db.Float,   nullable=True, default=0.0)

    fechaCaducidad    = db.Column(db.Date, nullable=True)
    estatus           = db.Column(
        db.Enum('Disponible', 'Caducado', 'Agotado', 'EnEspera', 'Cancelado'),
        nullable=False,
        default='Disponible',
    )

    # Relaciones
    materiaProveida = db.relationship(
        'MateriaProveida',
        backref=db.backref('lotes', lazy='dynamic'),
    )
    ordenCompra = db.relationship(
        'OrdenCompra',
        backref=db.backref('lotes', lazy='dynamic'),
    )
    # canalCorte se define via backref desde CanalCorte.lotes
