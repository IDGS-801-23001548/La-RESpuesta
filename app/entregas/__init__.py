from flask import Blueprint

entregas = Blueprint(
    "entregas",                  
    __name__,
    url_prefix="/entregas",
    template_folder='../templates/entregas'
)
