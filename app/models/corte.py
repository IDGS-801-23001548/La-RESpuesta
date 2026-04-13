from app.extensions import db


class Corte(db.Model):

    __tablename__   = 'corte'

    idCorte         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCategoria     = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'), nullable=False)
    idFoto          = db.Column(db.String(255), nullable=True)
    nombreCorte     = db.Column(db.String(50), nullable=False)
    Porcentaje      = db.Column(db.Float, nullable=True)
    precioPorKilo   = db.Column(db.Float, nullable=True, default=0.0)

    canalCortes = db.relationship(
        'CanalCorte',
        backref='corte',
        lazy='dynamic'
    )
