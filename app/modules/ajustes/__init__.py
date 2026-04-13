from flask import Blueprint

ajustes = Blueprint(
    "ajustes",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/ajustes'
)

from . import routes