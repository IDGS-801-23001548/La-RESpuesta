from app.extensions import db

class Persona(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre              = db.Column(db.String(100), nullable=False)
    apellido_paterno    = db.Column(db.String(100), nullable=False)
    apellido_materno    = db.Column(db.String(100))
    telefono            = db.Column(db.String(20))
    direccion           = db.Column(db.String(255))

    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'))