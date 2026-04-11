from flask import Blueprint

produccion = Blueprint(
    "produccion",
    __name__,
    url_prefix="/admin",
)

from . import routes
