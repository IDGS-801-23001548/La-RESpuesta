from flask import Blueprint

materia = Blueprint(
    "materia",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/materia'
)

from . import routes