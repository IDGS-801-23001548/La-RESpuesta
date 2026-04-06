from flask import Blueprint

productos = Blueprint(
    "productos",
    __name__,
    url_prefix="/admin",
    template_folder='../templates/productos'
)

from . import routes
