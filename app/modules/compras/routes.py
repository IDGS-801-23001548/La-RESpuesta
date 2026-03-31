from flask import render_template, redirect, url_for, flash, request
from . import compras
from app.extensions import db
from app.models import User
from app.modules.admin.forms import ComprasForm
from flask_security import login_required, current_user
from flask_security.decorators import roles_required

@compras.route("/compras", methods=['GET', 'POST'])

@roles_required('admin')
def compra():
    return render_template("admin/compras.html")

@compras.route("/compras/detalle", methods=['GET', 'POST'])

@roles_required('admin')
def compra_detalle():
    return render_template("admin/compras.html")

@compras.route("/compras/nueva", methods=['GET', 'POST'])

@roles_required('admin')
def compra_nueva():
    form = ComprasForm()
    return render_template("admin/compras_nueva.html", form = form)