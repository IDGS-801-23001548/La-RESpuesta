from flask_sqlalchemy import SQLAlchemy
from flask import request, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()

def limit_by_email():
    return request.form.get("email") or request.remote_addr

limiter = Limiter(get_remote_address, app=current_app)
