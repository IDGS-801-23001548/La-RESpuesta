from flask import Blueprint

finanzas = Blueprint(
    "finanzas",                  
    __name__,
    url_prefix="/finanzas",
    template_folder='../templates/admin/finanzas'
)

from . import routes