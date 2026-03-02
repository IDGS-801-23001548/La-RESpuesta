from app.extensions import db
from datetime import datetime

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