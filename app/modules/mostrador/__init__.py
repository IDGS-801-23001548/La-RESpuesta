from flask import Blueprint

mostrador = Blueprint(
    "mostrador",                  
    __name__,
    url_prefix="/mostrador",
    template_folder='../templates/mostrador'
)

from . import routes