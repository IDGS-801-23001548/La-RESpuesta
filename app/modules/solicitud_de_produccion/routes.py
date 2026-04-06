from flask import render_template, redirect, url_for, flash, request, render_template, current_app, make_response
from . import solicitud_de_produccion
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

@solicitud_de_produccion.route('/solicitudes')
@login_required
@roles_required('admin')
def solicitudes():
    return render_template('admin/solicitud_produccion/solicitudes.html', solicitudes=[])

@solicitud_de_produccion.route('/solicitudes/nueva')
@login_required
@roles_required('admin')
def solicitudes_nueva():
    return render_template('admin/solicitud_produccion/solicitudes_form.html', solicitud=None)

@solicitud_de_produccion.route('/solicitudes/<int:id>/editar')
@login_required
@roles_required('admin')
def solicitudes_editar(id):
    return render_template('admin/solicitud_produccion/solicitudes_form.html', solicitud=None)

@solicitud_de_produccion.route('/solicitudes/<int:id>/cancelar', methods=['POST'])
@login_required
@roles_required('admin')
def solicitudes_cancelar(id):
    return redirect(url_for('solicitud_de_produccion.solicitudes'))