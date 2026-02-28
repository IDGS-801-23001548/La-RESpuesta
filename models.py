from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'

    id_rol        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_rol    = db.Column(db.String(50), unique=True, nullable=False)
    descripcion   = db.Column(db.Text)

    # back_populates apunta al atributo 'rol' en User
    usuarios      = db.relationship('User', back_populates='rol', lazy=True)
    permisos      = db.relationship('ModulePermission', backref='role', lazy=True)


class User(db.Model):
    __tablename__ = 'usuarios'

    id_usuario        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario    = db.Column(db.String(50), unique=True, nullable=False)
    password_hash     = db.Column(db.String(255), nullable=False)

    # ── FK obligatoria para que SQLAlchemy pueda hacer el JOIN ──
    id_rol            = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=True)

    # back_populates apunta al atributo 'usuarios' en Role
    rol               = db.relationship('Role', back_populates='usuarios')

    estatus           = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    intentos_fallidos = db.Column(db.Integer, default=0)
    fecha_bloqueo     = db.Column(db.DateTime, nullable=True)
    ultimo_login      = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ModulePermission(db.Model):
    __tablename__ = 'permisos_modulos'

    id_permiso      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_rol          = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False)
    modulo          = db.Column(db.String(50), nullable=False)
    l_lectura       = db.Column(db.Boolean, default=False)
    a_alta          = db.Column(db.Boolean, default=False)
    b_baja          = db.Column(db.Boolean, default=False)
    m_modificacion  = db.Column(db.Boolean, default=False)


class Log(db.Model):
    __tablename__ = 'logs_sistema'

    id_log        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario    = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    tipo_evento   = db.Column(
                        db.Enum('Seguridad', 'Inventario', 'Ventas', 'Configuracion'),
                        nullable=False
                    )
    accion        = db.Column(db.String(100), nullable=False)
    descripcion   = db.Column(db.Text)
    id_referencia = db.Column(db.Integer, nullable=True)
    fecha_hora    = db.Column(db.DateTime, default=datetime.now)
    ip_origen     = db.Column(db.String(45))