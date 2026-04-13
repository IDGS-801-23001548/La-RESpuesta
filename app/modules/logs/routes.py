from flask import render_template, request, render_template, make_response
from . import log
from flask_security import login_required
from flask_security.decorators import roles_required
import re
import csv
import io
from datetime import datetime
from pathlib import Path
from flask_login import login_required
from flask_security import roles_required

LOG_PATH = Path("app.log")
POR_PAGINA = 15

# ─────────────────────────────────────────────────────────────────────────────
#  Parser de línea de log
#  Formato esperado: 2026-03-31 19:17:27,686 - INFO - mensaje
# ─────────────────────────────────────────────────────────────────────────────
PATRON = re.compile(
    r"^(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - (?P<nivel>INFO|WARNING|DEBUG|ERROR|CRITICAL) - (?P<mensaje>.+)$"
)

# Clasificación de eventos según palabras clave en el mensaje
# IMPORTANTE: el orden importa — la primera coincidencia gana
TIPOS = [
    ("login_ok",    re.compile(r"login exitoso|loggin exitoso", re.I)),
    ("login_fail",  re.compile(r"intento fallido", re.I)),
    ("bloqueado",   re.compile(r"bloqueado por intentos|cuenta bloqueada|intento en cuenta bloqueada", re.I)),
    ("compra",      re.compile(r"orden de compra|orden .+ registrada|recepci[oó]n confirmada|orden .+ cancelada", re.I)),
    ("pago",        re.compile(r"pago a proveedor|orden .+ pagada", re.I)),
    ("produccion",  re.compile(r"producci[oó]n completada|producci[oó]n autorizada", re.I)),
    ("solicitud",   re.compile(r"solicitud de producci[oó]n|solicitud .+ creada|solicitud .+ cancelada", re.I)),
    ("receta",      re.compile(r"receta .+ creada|receta .+ actualizada|receta .+ eliminada", re.I)),
    ("proveedor",   re.compile(r"proveedor .+ creado|proveedor .+ actualizado|proveedor .+ eliminado|proveedor .+ estado:", re.I)),
    ("finanzas",    re.compile(r"movimiento financiero", re.I)),
    ("venta",       re.compile(r"venta_mostrador", re.I)),
    ("pedido",      re.compile(r"pedido_entregado", re.I)),
    ("creacion",    re.compile(r"creado", re.I)),
    ("edicion",     re.compile(r"actualizado", re.I)),
    ("estado",      re.compile(r"estado:", re.I)),
    ("eliminado",   re.compile(r"eliminado", re.I)),
    ("sesion",      re.compile(r"sesi[oó]n inv[aá]lida|tokens de sesi[oó]n", re.I)),
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

@log.route("/logs")
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
        "error":   sum(1 for e in todas if e["nivel"] == "ERROR"),
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


@log.route("/logs/export")
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
