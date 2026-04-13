from flask import Blueprint

venta = Blueprint(
    "venta",                  
    __name__,
    url_prefix="/venta",
    template_folder='../templates/venta'
)

from . import routes