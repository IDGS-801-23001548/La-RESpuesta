from app.extensions import db


class CanalCorte(db.Model):

    __tablename__       = 'canal_corte'

    idPropio            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCorte             = db.Column(db.Integer, db.ForeignKey('corte.idCorte'), nullable=False)
    idCanal             = db.Column(db.Integer, db.ForeignKey('canal.idCanal'), nullable=False)
    idLote              = db.Column(db.Integer, db.ForeignKey('lote.idLote'), nullable=False)
    CantidadEsperada    = db.Column(db.Float, nullable=True)
    CantidadObtenida    = db.Column(db.Float, nullable=True)
    Merma               = db.Column(db.Float, nullable=True)
