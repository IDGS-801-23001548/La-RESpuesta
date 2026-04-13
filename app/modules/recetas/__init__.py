from flask import Blueprint

receta = Blueprint(
    "receta",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/recetas'
)

from . import routes