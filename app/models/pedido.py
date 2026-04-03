from app.extensions import db

class Pedido(db.Model):

    __tablename__               = 'pedido'
    idPedido                    = db.Column(db.Integer, primary_key=True)
    idUsuario                   = db.Column(db.Integer, db.ForeignKey('user.id'))
    Total                       = db.Column(db.Float)
    Tipo                        = db.Column(db.String(50), nullable=True)
    Estatus                     = db.Column(db.String(50), nullable=True)
    Entrega                     = db.Column(db.String(50), nullable=True)

    unidadesPedido                    = db.relationship('ProductoUnitario',
                                        backref='pedido',
                                        lazy='dynamic')