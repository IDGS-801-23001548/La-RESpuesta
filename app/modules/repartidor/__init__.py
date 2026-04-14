from flask import Blueprint

repartidor_bp = Blueprint('repartidor', __name__, url_prefix='/repartidor')

from . import routes