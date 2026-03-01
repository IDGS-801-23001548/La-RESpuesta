from app.extensions import db

from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario      = db.Column(db.String(50), unique=True, nullable=False)
    password_hash       = db.Column(db.String(255), nullable=False)

    # ── FK obligatoria para que SQLAlchemy pueda hacer el JOIN ──
    id_rol              = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=True)

    # back_populates apunta al atributo 'usuarios' en Rol
    rol                 = db.relationship('Rol', back_populates='usuarios')

    estatus             = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    intentos_fallidos   = db.Column(db.Integer, default=0)
    fecha_bloqueo       = db.Column(db.DateTime, nullable=True)
    ultimo_login        = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)