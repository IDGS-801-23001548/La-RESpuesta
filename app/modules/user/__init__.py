from flask import Blueprint

user = Blueprint(
    "user",                  
    __name__,
    url_prefix="/admin",
    template_folder='../templates/user'
)

from . import routes