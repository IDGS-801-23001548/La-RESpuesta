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

@admin.route('/materia-prima')
def materia():
    return render_template('admin/materia.html')

@admin.route('/materia-prima/nueva')
def materia_nueva():
    return render_template('admin/materia_form.html', materia=None)

@admin.route('/materia-prima/<int:id>/editar')
def materia_editar(id):
    return render_template('admin/materia_form.html', materia=None)

@admin.route('/materia-prima/<int:id>/eliminar', methods=['POST'])
def materia_eliminar(id):
    return redirect(url_for('materia'))

@admin.route('/proveedores')
def proveedores():
    return render_template('admin/proveedores.html')

@admin.route('/proveedores/nuevo')
def proveedores_nuevo():
    form = User()
    return render_template('admin/proveedores_form.html', proveedor=None, form = form)

@admin.route('/proveedores/detalle')
def proveedores_detalle():
    return render_template('admin/proveedores_detalle.html', proveedor=None)

@admin.route('/proveedores/<int:id>/editar')
def proveedores_editar(id):
    form = ComprasForm()
    return render_template('admin/proveedores_form.html', proveedor=None, form = form)

@admin.route('/proveedores/<int:id>/eliminar', methods=['POST'])
def proveedores_eliminar(id):
    return redirect(url_for('proveedores'))

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
# ── Ajusta esta ruta al path real de tu archivo de logs ───────────────────────
LOG_PATH = Path("app.log")
POR_PAGINA = 15

# ─────────────────────────────────────────────────────────────────────────────
#  Parser de línea de log
#  Formato esperado: 2026-03-31 19:17:27,686 - INFO - mensaje
# ─────────────────────────────────────────────────────────────────────────────
PATRON = re.compile(
    r"^(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - (?P<nivel>INFO|WARNING|DEBUG|ERROR) - (?P<mensaje>.+)$"
)

# Clasificación de eventos según palabras clave en el mensaje
TIPOS = [
    ("login_ok",   re.compile(r"login exitoso|loggin exitoso", re.I)),
    ("login_fail", re.compile(r"intento fallido", re.I)),
    ("bloqueado",  re.compile(r"bloqueado por intentos|cuenta bloqueada|intento en cuenta bloqueada", re.I)),
    ("creacion",   re.compile(r"creado", re.I)),
    ("edicion",    re.compile(r"actualizado", re.I)),
    ("estado",     re.compile(r"estado:", re.I)),
    ("eliminado",  re.compile(r"eliminado", re.I)),
    ("sesion",     re.compile(r"sesi[oó]n inv[aá]lida|tokens de sesi[oó]n", re.I)),
]

IP_RE = re.compile(r"ip=(\d{1,3}(?:\.\d{1,3}){3})")


def clasificar(mensaje: str) -> str:
    for tipo, patron in TIPOS:
        if patron.search(mensaje):
            return tipo
    return "sistema"


def parsear_logs() -> list[dict]:
    """Lee y parsea todas las líneas del archivo de logs."""
    entradas = []
    if not LOG_PATH.exists():
        return entradas

    with LOG_PATH.open(encoding="utf-8", errors="replace") as f:
        for linea in f:
            m = PATRON.match(linea.strip())
            if not m:
                continue
            mensaje = m.group("mensaje")
            ip_match = IP_RE.search(mensaje)
            entradas.append({
                "fecha":   m.group("fecha"),
                "nivel":   m.group("nivel"),
                "mensaje": mensaje,
                "tipo":    clasificar(mensaje),
                "ip":      ip_match.group(1) if ip_match else None,
            })

    return list(reversed(entradas))  # más reciente primero


def aplicar_filtros(entradas: list[dict], filtros: dict) -> list[dict]:
    """Aplica todos los filtros activos sobre la lista de entradas."""

    if filtros.get("q"):
        q = filtros["q"].lower()
        entradas = [e for e in entradas if q in e["mensaje"].lower()]

    if filtros.get("nivel"):
        entradas = [e for e in entradas if e["nivel"] == filtros["nivel"]]

    if filtros.get("tipo"):
        entradas = [e for e in entradas if e["tipo"] == filtros["tipo"]]

    if filtros.get("desde"):
        try:
            desde = datetime.strptime(filtros["desde"], "%Y-%m-%d")
            entradas = [e for e in entradas
                        if datetime.strptime(e["fecha"], "%Y-%m-%d %H:%M:%S") >= desde]
        except ValueError:
            pass

    if filtros.get("hasta"):
        try:
            hasta = datetime.strptime(filtros["hasta"] + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            entradas = [e for e in entradas
                        if datetime.strptime(e["fecha"], "%Y-%m-%d %H:%M:%S") <= hasta]
        except ValueError:
            pass

    return entradas


# ─────────────────────────────────────────────────────────────────────────────
#  Rutas
# ─────────────────────────────────────────────────────────────────────────────

@admin.route("/logs")
@login_required
@roles_required('admin')
def logs():
    filtros = {
        "q":     request.args.get("q", "").strip(),
        "nivel": request.args.get("nivel", ""),
        "tipo":  request.args.get("tipo", ""),
        "desde": request.args.get("desde", ""),
        "hasta": request.args.get("hasta", ""),
    }
    pagina = max(1, request.args.get("pagina", 1, type=int))

    todas = parsear_logs()
    filtradas = aplicar_filtros(todas, filtros)

    # Conteo por nivel (sobre el total sin filtrar)
    conteo = {
        "info":    sum(1 for e in todas if e["nivel"] == "INFO"),
        "warning": sum(1 for e in todas if e["nivel"] == "WARNING"),
        "debug":   sum(1 for e in todas if e["nivel"] == "DEBUG"),
    }

    # Paginación
    total = len(filtradas)
    total_paginas = max(1, (total + POR_PAGINA - 1) // POR_PAGINA)
    pagina = min(pagina, total_paginas)
    inicio = (pagina - 1) * POR_PAGINA
    logs_pagina = filtradas[inicio: inicio + POR_PAGINA]

    return render_template(
        "admin/logs/logs.html",
        logs=logs_pagina,
        total=total,
        conteo=conteo,
        filtros=filtros,
        pagina=pagina,
        total_paginas=total_paginas,
    )


@admin.route("/logs/export")
@login_required
@roles_required('admin')
def logs_export():
    """Exporta los logs filtrados como CSV."""
    filtros = {
        "q":     request.args.get("q", "").strip(),
        "nivel": request.args.get("nivel", ""),
        "tipo":  request.args.get("tipo", ""),
        "desde": request.args.get("desde", ""),
        "hasta": request.args.get("hasta", ""),
    }

    entradas = aplicar_filtros(parsear_logs(), filtros)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["fecha", "nivel", "tipo", "ip", "mensaje"])
    writer.writeheader()
    writer.writerows(entradas)

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=logs.csv"
    return response

@admin.route("/ajustes", methods=['GET', 'POST'])
def ajustes():
    return render_template("admin/ajustes.html")