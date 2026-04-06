from flask import Blueprint

solicitud_de_produccion = Blueprint(
    "solicitud_de_produccion",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/solicitud_produccion'
)

from . import routes