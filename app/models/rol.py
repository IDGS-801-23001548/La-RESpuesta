from app.extensions import db
#Importamos la clase RoleMixin de flask_security
from flask_security import RoleMixin

class Role(RoleMixin, db.Model):
 
    __tablename__   = 'role'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(80), nullable=False)
    description     =  db.Column(db.String(255))