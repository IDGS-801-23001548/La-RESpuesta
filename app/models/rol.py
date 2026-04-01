from app.extensions import db

class Rol(db.Model):
<<<<<<< HEAD
    __tablename__ = 'roles'
=======
    __tablename__ = 'role'
>>>>>>> develop

    id_rol          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_rol      = db.Column(db.String(50), unique=True, nullable=False)
    descripcion     = db.Column(db.Text)
<<<<<<< HEAD
    usuarios         = db.relationship('Usuario', back_populates='rol')
=======
    usuarios        = db.relationship('Usuario', back_populates='role')
>>>>>>> develop
