from app.extensions import db


class CorteUnitario(db.Model):
    """Registro de venta de corte por peso.

    Analogo a ProductoUnitario pero orientado a kilos en vez de unidades.
    Cuando el cliente agrega un corte al carrito se:
      1. Busca el primer lote disponible (FIFO por fechaCaducidad) que
         tenga ese corte (via canal_corte).
      2. Se descuenta el peso del lote.totalMateria.
      3. Se crea este registro con estatus 'EnCarrito'.

    Al confirmar el pedido pasa a 'Vendido' y se asocia al idPedido.
    Si se cancela el pedido o se quita del carrito, se devuelve el peso
    al lote y se elimina/cancela este registro.
    """

    __tablename__        = 'corte_unitario'

    idCorteUnitario      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCorte              = db.Column(db.Integer, db.ForeignKey('corte.idCorte'), nullable=False)
    idLote               = db.Column(db.Integer, db.ForeignKey('lote.idLote'), nullable=True)
    idCarrito            = db.Column(db.Integer, db.ForeignKey('carrito.idCarrito'), nullable=True)
    idPedido             = db.Column(db.Integer, db.ForeignKey('pedido.idPedido'), nullable=True)
    peso                 = db.Column(db.Float, nullable=False)          # kg solicitados
    costo                = db.Column(db.Float, nullable=False)          # precioPorKilo * peso
    estatus              = db.Column(
        db.String(20), nullable=False, default='EnCarrito'
    )  # EnCarrito | Vendido | Cancelado

    # Relaciones
    corte = db.relationship(
        'Corte',
        backref=db.backref('ventasUnitarias', lazy='dynamic'),
    )
    lote = db.relationship(
        'Lote',
        backref=db.backref('cortesVendidos', lazy='dynamic'),
    )
