from flask import Blueprint

proveedor = Blueprint(
    "proveedor",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/admin/proveedor'
)

from . import routes