from app.extensions import db


# Estatus de un canal_corte:
#   Disponible → recien creado al comprar la canal, aun no se ha procesado
#                con una receta de corte
#   Consumido  → ya paso por una receta de corte y genero un Lote
ESTATUS_CANAL_CORTE = ('Disponible', 'Consumido')


class CanalCorte(db.Model):

    __tablename__       = 'canal_corte'

    idCanalCorte        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCorte             = db.Column(db.Integer, db.ForeignKey('corte.idCorte'), nullable=False)
    idCanal             = db.Column(db.Integer, db.ForeignKey('canal.idCanal'), nullable=False)
    CantidadEsperada    = db.Column(db.Float, nullable=True)
    CantidadObtenida    = db.Column(db.Float, nullable=True)
    Merma               = db.Column(db.Float, nullable=True)
    estatus             = db.Column(db.String(20), nullable=False, default='Disponible')

    lotes = db.relationship(
        'Lote',
        backref='canalCorte',
        lazy='dynamic',
        foreign_keys='Lote.idCanalCorte',
    )
