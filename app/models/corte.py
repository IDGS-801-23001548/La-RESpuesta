from app.extensions import db


class Corte(db.Model):

    __tablename__   = 'corte'

    idCorte         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreCorte     = db.Column(db.String(50), nullable=False)
    Porcentaje      = db.Column(db.Float, nullable=True)

    canalCortes = db.relationship(
        'CanalCorte',
        backref='corte',
        lazy='dynamic'
    )
