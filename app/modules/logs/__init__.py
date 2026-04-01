from flask import Blueprint

log = Blueprint(
    "log",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/admin/logs'
)

from . import routes