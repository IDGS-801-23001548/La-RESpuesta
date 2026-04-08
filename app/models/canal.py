from app.extensions import db


class Canal(db.Model):

    __tablename__   = 'canal'

    idCanal         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdCategoria     = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'), nullable=False)
    Descripcion     = db.Column(db.String(200), nullable=True)
    Peso            = db.Column(db.Float, nullable=True)

    categoria = db.relationship(
        'Categoria',
        backref=db.backref('canales', lazy='dynamic')
    )

    canalCortes = db.relationship(
        'CanalCorte',
        backref='canal',
        lazy='dynamic'
    )
