from flask import Blueprint

compras = Blueprint(
    "compras",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/compras'
)

from . import routes