from app.extensions import db

class Rol(db.Model):
    __tablename__ = 'role'

    id_rol          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_rol      = db.Column(db.String(50), unique=True, nullable=False)
    descripcion     = db.Column(db.Text)
    usuarios        = db.relationship('Usuario', back_populates='role')