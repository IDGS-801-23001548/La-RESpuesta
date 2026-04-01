from flask import Blueprint

auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/security',
    template_folder='../templates/security'
)

from . import routes