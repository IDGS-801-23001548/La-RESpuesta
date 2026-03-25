from flask import Blueprint

entregas_bp = Blueprint(
    "entregas",                  
    __name__,
    url_prefix="/entregas",
    template_folder='../templates/entregas'
)
