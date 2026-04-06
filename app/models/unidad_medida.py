from app.extensions import db

class UnidadMedida(db.Model):

    __tablename__       = 'unidad_medida'
    idUnidadMedida      = db.Column(db.Integer, primary_key=True)
    nombreUnidadMedida  = db.Column(db.String(25), nullable=False)
    idConversor         = db.Column(db.Integer, db.ForeignKey('conversor.idConversor'), nullable=True)

    materiasProveidas   = db.relationship(
        'MateriaProveida',
        backref='unidadMedida',
        lazy='dynamic'
    )
