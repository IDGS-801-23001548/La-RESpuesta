from flask import request
from extensions import db
from models import Log

def registrar_log(tipo, accion, descripcion, user_id=None):
    nuevo_log = Log(
        tipo_evento=tipo,
        accion=accion,
        descripcion=descripcion,
        id_usuario=user_id,
        ip_origen=request.remote_addr
    )

    db.session.add(nuevo_log)