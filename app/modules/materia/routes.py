from flask import render_template, redirect, url_for, flash, request, render_template, current_app, make_response
from . import materia
from app.extensions import db
from app.models import User
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
import re
import csv
import io
from datetime import datetime
from pathlib import Path
from flask_login import login_required
from flask_security import roles_required

@materia.route('/materia-prima')
@login_required
@roles_required('admin')
def materias():
    return render_template('admin/materia/materia.html')

@materia.route('/materia-prima/nueva')
@login_required
@roles_required('admin')
def materia_nueva():
    return render_template('admin/materia/materia_form.html', materia=None)

@materia.route('/materia-prima/<int:id>/editar')
@login_required
@roles_required('admin')
def materia_editar(id):
    return render_template('admin/materia/materia_form.html', materia=None)

@materia.route('/materia-prima/<int:id>/eliminar', methods=['POST'])
@login_required
@roles_required('admin')
def materia_eliminar(id):
    return redirect(url_for('materia'))