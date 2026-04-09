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


@admin.route('/produccion')
def produccion():
    return render_template('admin/produccion.html',
                           ordenes=[], solicitudes_pendientes=[], kg_producidos=0)

@admin.route('/produccion/nueva')
def produccion_nueva():
    return render_template('admin/produccion_form.html', solicitud=None)

@admin.route('/produccion/desde-solicitud/<int:id>')
def produccion_desde_solicitud(id):
    return render_template('admin/produccion_form.html', solicitud=None)

@admin.route('/produccion/<int:id>')
def produccion_detalle(id):
    return render_template('admin/produccion_detalle.html', orden=None)

@admin.route('/produccion/<int:id>/completar', methods=['GET', 'POST'])
def produccion_completar(id):
    return redirect(url_for('admin.produccion_detalle', id=id))

# ── RUTAS A DESARROLLAR ──────────────────────────────────────────

@admin.route("/utilidad", methods=['GET', 'POST'])
def utilidad():
    return render_template("admin/utilidad.html")

@admin.route("/reportes", methods=['GET', 'POST'])
def reportes():
    return render_template("admin/reportes.html")

@admin.route("/ventas")
def ventas():
    return f"ventas"