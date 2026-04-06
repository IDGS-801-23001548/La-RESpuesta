from app.extensions import db

class Conversor(db.Model):

    __tablename__    = 'conversor'
    idConversor      = db.Column(db.Integer, primary_key=True)
    nombreConversor  = db.Column(db.String(25), nullable=False, unique=True)

    unidadesMedida   = db.relationship(
        'UnidadMedida',
        backref='conversor',
        lazy='dynamic'
    )
