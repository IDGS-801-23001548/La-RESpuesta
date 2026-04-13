from flask import render_template, redirect, url_for, flash, request, render_template, current_app, make_response
from . import admin
from app.extensions import db
from app.models import User
from app.modules.admin.forms import ComprasForm
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
import re
import csv
import io
from datetime import datetime
from pathlib import Path
from flask_login import login_required
from flask_security import roles_required

@admin.route("/index")
def index():
    return f"index"

@admin.route("/dashboard", methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def dashboard():
    return render_template("admin/dashboard.html")
