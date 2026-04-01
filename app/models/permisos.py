from app.extensions import db

class ModuloPermisos(db.Model):
    __tablename__ = 'permisos_modulos'

    id_permiso      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    modulo          = db.Column(db.String(50), nullable=False)
    l_lectura       = db.Column(db.Boolean, default=False)
    a_alta          = db.Column(db.Boolean, default=False)
    b_baja          = db.Column(db.Boolean, default=False)
    m_modificacion  = db.Column(db.Boolean, default=False)