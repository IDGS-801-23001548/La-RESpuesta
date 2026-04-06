from flask import render_template, redirect, url_for, flash, request, render_template, current_app, make_response
from . import receta
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

@receta.route('/recetas')
@login_required
@roles_required('admin')
def recetas():
    return render_template('admin/recetas/recetas.html', recetas=[])

@receta.route('/recetas/nueva')
@login_required
@roles_required('admin')
def recetas_nueva():
    return render_template('admin/recetas/recetas_form.html', receta=None)

@receta.route('/recetas/<int:id>/editar')
@login_required
@roles_required('admin')
def recetas_editar(id):
    return render_template('admin/recetas/recetas_form.html', receta=None)

@receta.route('/recetas/<int:id>/eliminar', methods=['POST'])
@login_required
@roles_required('admin')
def recetas_eliminar(id):
    return redirect(url_for('recetas'))