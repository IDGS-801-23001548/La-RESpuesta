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

@admin.route('/recetas')
def recetas():
    return render_template('admin/recetas.html', recetas=[])

@admin.route('/recetas/nueva')
def recetas_nueva():
    return render_template('admin/recetas_form.html', receta=None)

@admin.route('/recetas/<int:id>/editar')
def recetas_editar(id):
    return render_template('admin/recetas_form.html', receta=None)

@admin.route('/recetas/<int:id>/eliminar', methods=['POST'])
def recetas_eliminar(id):
    return redirect(url_for('recetas'))

@admin.route('/solicitudes')
def solicitudes():
    return render_template('admin/solicitudes.html', solicitudes=[])

@admin.route('/solicitudes/nueva')
def solicitudes_nueva():
    return render_template('admin/solicitudes_form.html', solicitud=None)

@admin.route('/solicitudes/<int:id>/editar')
def solicitudes_editar(id):
    return render_template('admin/solicitudes_form.html', solicitud=None)

@admin.route('/solicitudes/<int:id>/cancelar', methods=['POST'])
def solicitudes_cancelar(id):
    return redirect(url_for('admin.solicitudes'))

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


@admin.route('/productos')
def productos():
    return render_template('admin/productos.html',
                           productos=[], kg_totales=0)

@admin.route('/productos/ajuste', methods=['GET', 'POST'])
def productos_ajuste():
    return render_template('admin/productos_ajuste.html', producto=None)

@admin.route('/ventas')
def ventas():
    return render_template('admin/ventas.html',
        ventas=[],
        total_hoy='0.00',
        tickets_hoy=0,
        kg_hoy=0,
        ticket_promedio='0.00',
        ventas_por_canal={},
        tickets_por_canal={}
    )


@admin.route('/pago')
def pago():
    return render_template('admin/pagos.html',
        proveedores=[], pagos=[],
        total_pendiente='0.00', proveedores_con_saldo=0,
        pagado_mes='0.00', num_pagos_mes=0)

@admin.route('/pagos/nuevo', methods=['GET', 'POST'])
def pagos_nuevo():
    proveedor_id = request.args.get('proveedor_id')
    return render_template('admin/pagos_form.html', proveedor_id=proveedor_id)

@admin.route('/pagos/proveedor/<int:id>')
def pagos_cuenta(id):
    return render_template('admin/pagos_cuenta.html',
        proveedor=None, movimientos=[])

@admin.route('/corte')
def corte_diario():
    return render_template('admin/corte_diario.html',
        cortes=[],
        corte_hoy_existe=False,
        corte_hoy_id=None,
        ventas_mes='0.00',
        utilidad_mes='0.00',
        dias_sin_corte=0
    )

@admin.route('/corte/diario/<int:id>')
def corte_detalle(id):
    return render_template('admin/corte_detalle.html', corte=None)

@admin.route('/corte-diario/generar', methods=['POST'])
def corte_generar():
    return redirect(url_for('admin.corte_diario'))

# ── RUTAS A DESARROLLAR ──────────────────────────────────────────

@admin.route("/utilidad", methods=['GET', 'POST'])
def utilidad():
    return render_template("admin/utilidad.html")

@admin.route("/reportes", methods=['GET', 'POST'])
def reportes():
    return render_template("admin/reportes.html")

@admin.route("/ajustes",)
def ajustes():
    return f"ajustes"