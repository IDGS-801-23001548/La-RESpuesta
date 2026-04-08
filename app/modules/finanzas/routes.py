from datetime import datetime, date, timedelta

from flask import render_template, redirect, url_for, flash, request
from flask_security import login_required, current_user
from sqlalchemy import func, extract

from . import finanzas
from app.extensions import db
from app.models import Pedido, OrdenCompra, Retiro


# ─────────────────────────────────────────────────────────────────
# Helpers de rango de fechas
# ─────────────────────────────────────────────────────────────────
def _parse_rango():
    """
    Lee ?preset=hoy|semana|mes|rango y ?desde / ?hasta del query string.
    Devuelve (desde: date, hasta: date, preset: str).
    """
    preset = (request.args.get('preset') or 'hoy').lower()
    hoy = date.today()

    if preset == 'hoy':
        return hoy, hoy, 'hoy'

    if preset == 'semana':
        # Lunes de esta semana → hoy
        inicio = hoy - timedelta(days=hoy.weekday())
        return inicio, hoy, 'semana'

    if preset == 'mes':
        return hoy.replace(day=1), hoy, 'mes'

    # preset == 'rango' (o desconocido) → usa desde/hasta
    try:
        desde = datetime.strptime(request.args.get('desde', ''), '%Y-%m-%d').date()
    except ValueError:
        desde = hoy
    try:
        hasta = datetime.strptime(request.args.get('hasta', ''), '%Y-%m-%d').date()
    except ValueError:
        hasta = hoy
    if hasta < desde:
        desde, hasta = hasta, desde
    return desde, hasta, 'rango'


def _bounds(desde, hasta):
    ini = datetime.combine(desde, datetime.min.time())
    fin = datetime.combine(hasta, datetime.max.time())
    return ini, fin


# ═════════════════════════════════════════════════════════════════
# BALANCE FINANCIERO  (antes "Corte Diario")
# ═════════════════════════════════════════════════════════════════
@finanzas.route('/corte-diario')
@login_required
def corte_diario():
    desde, hasta, preset = _parse_rango()
    ini, fin = _bounds(desde, hasta)

    # ── ENTRADAS (Pedidos no cancelados) ───────────────────────
    pedidos = (Pedido.query
               .filter(Pedido.fechaCreacion >= ini,
                       Pedido.fechaCreacion <= fin,
                       Pedido.Estatus != 'Cancelado')
               .all())

    entradas_efectivo = sum((p.Total or 0) for p in pedidos if p.Tipo == 'Efectivo')
    entradas_tarjeta  = sum((p.Total or 0) for p in pedidos if p.Tipo == 'Tarjeta')
    entradas_transfer = sum((p.Total or 0) for p in pedidos if p.Tipo == 'Transferencia')
    entradas_banco    = entradas_tarjeta + entradas_transfer
    num_ventas        = len(pedidos)

    # ── SALIDAS por pago a proveedores ─────────────────────────
    pagos = (OrdenCompra.query
             .filter(OrdenCompra.PagoProveedor == 'Pagado',
                     OrdenCompra.fechaPago >= ini,
                     OrdenCompra.fechaPago <= fin)
             .all())

    salidas_prov_efectivo = sum((o.totalOrden or 0) for o in pagos if o.metodoPago == 'Efectivo')
    salidas_prov_transfer = sum((o.totalOrden or 0) for o in pagos if o.metodoPago == 'Transferencia')
    num_pagos_prov        = len(pagos)

    # ── Movimientos manuales (ingresos / retiros) ──────────────
    movimientos = (Retiro.query
                   .filter(Retiro.fecha >= ini, Retiro.fecha <= fin)
                   .order_by(Retiro.fecha.desc())
                   .all())

    retiros_efectivo  = sum(m.monto for m in movimientos if m.tipo == 'Retiro'  and m.origen == 'Efectivo')
    retiros_transfer  = sum(m.monto for m in movimientos if m.tipo == 'Retiro'  and m.origen == 'Transferencia')
    ingresos_efectivo = sum(m.monto for m in movimientos if m.tipo == 'Ingreso' and m.origen == 'Efectivo')
    ingresos_transfer = sum(m.monto for m in movimientos if m.tipo == 'Ingreso' and m.origen == 'Transferencia')

    # ── Totales por canal ──────────────────────────────────────
    entradas_efectivo_total = entradas_efectivo + ingresos_efectivo
    entradas_banco_total    = entradas_banco    + ingresos_transfer
    total_entradas          = entradas_efectivo_total + entradas_banco_total

    salidas_efectivo = salidas_prov_efectivo + retiros_efectivo
    salidas_banco    = salidas_prov_transfer + retiros_transfer
    total_salidas    = salidas_efectivo + salidas_banco

    balance_efectivo = entradas_efectivo_total - salidas_efectivo
    balance_banco    = entradas_banco_total    - salidas_banco
    balance_total    = balance_efectivo        + balance_banco

    return render_template(
        'admin/finanzas/corte_diario.html',
        # rango
        desde=desde, hasta=hasta, preset=preset,
        # entradas
        entradas_efectivo=entradas_efectivo,
        entradas_tarjeta=entradas_tarjeta,
        entradas_transfer=entradas_transfer,
        entradas_banco=entradas_banco,
        total_entradas=total_entradas,
        num_ventas=num_ventas,
        # salidas
        salidas_prov_efectivo=salidas_prov_efectivo,
        salidas_prov_transfer=salidas_prov_transfer,
        num_pagos_prov=num_pagos_prov,
        movimientos=movimientos,
        retiros_efectivo=retiros_efectivo,
        retiros_transfer=retiros_transfer,
        ingresos_efectivo=ingresos_efectivo,
        ingresos_transfer=ingresos_transfer,
        salidas_efectivo=salidas_efectivo,
        salidas_banco=salidas_banco,
        total_salidas=total_salidas,
        # balance final
        balance_efectivo=balance_efectivo,
        balance_banco=balance_banco,
        balance_total=balance_total,
    )


# ═════════════════════════════════════════════════════════════════
# RETIROS
# ═════════════════════════════════════════════════════════════════
@finanzas.route('/movimientos/nuevo', methods=['POST'])
@login_required
def movimiento_nuevo():
    try:
        monto = float(request.form.get('monto') or 0)
    except ValueError:
        monto = 0
    tipo   = (request.form.get('tipo') or '').strip()
    origen = (request.form.get('origen') or '').strip()
    motivo = (request.form.get('motivo') or '').strip() or None

    if monto <= 0:
        flash('El monto debe ser mayor a 0.', 'danger')
        return redirect(request.referrer or url_for('finanzas.corte_diario'))
    if tipo not in ('Ingreso', 'Retiro'):
        flash('Selecciona el tipo de movimiento (Ingreso o Retiro).', 'danger')
        return redirect(request.referrer or url_for('finanzas.corte_diario'))
    if origen not in ('Efectivo', 'Transferencia'):
        flash('Selecciona el origen (Efectivo o Transferencia).', 'danger')
        return redirect(request.referrer or url_for('finanzas.corte_diario'))

    mov = Retiro(
        tipo=tipo,
        origen=origen,
        monto=monto,
        motivo=motivo,
        usuario=current_user.email if current_user.is_authenticated else 'sistema',
    )
    db.session.add(mov)
    db.session.commit()
    flash(f'{tipo} de ${monto:.2f} registrado ({origen}).', 'success')
    return redirect(request.referrer or url_for('finanzas.corte_diario'))


@finanzas.route('/movimientos/<int:id>/eliminar', methods=['POST'])
@login_required
def movimiento_eliminar(id):
    mov = Retiro.query.get_or_404(id)
    db.session.delete(mov)
    db.session.commit()
    flash('Movimiento eliminado.', 'success')
    return redirect(request.referrer or url_for('finanzas.corte_diario'))


# ═════════════════════════════════════════════════════════════════
# PAGO A PROVEEDORES
# ═════════════════════════════════════════════════════════════════
@finanzas.route('/pago-proveedores')
@login_required
def pago_proveedores():
    pendientes = (OrdenCompra.query
                  .filter(OrdenCompra.PagoProveedor == 'Pendiente',
                          OrdenCompra.estatus != 'Cancelada')
                  .order_by(OrdenCompra.fechaDeOrden.asc())
                  .all())

    pagadas = (OrdenCompra.query
               .filter(OrdenCompra.PagoProveedor == 'Pagado')
               .order_by(OrdenCompra.fechaPago.desc())
               .limit(20)
               .all())

    total_pendiente = sum(o.totalOrden or 0 for o in pendientes)
    proveedores_con_saldo = len({o.idProveedor for o in pendientes})

    hoy = date.today()
    pagado_mes = (db.session.query(func.coalesce(func.sum(OrdenCompra.totalOrden), 0))
                  .filter(OrdenCompra.PagoProveedor == 'Pagado',
                          extract('year',  OrdenCompra.fechaPago) == hoy.year,
                          extract('month', OrdenCompra.fechaPago) == hoy.month)
                  .scalar() or 0)

    return render_template(
        'admin/finanzas/pago_proveedores.html',
        pendientes=pendientes,
        pagadas=pagadas,
        total_pendiente=total_pendiente,
        proveedores_con_saldo=proveedores_con_saldo,
        pagado_mes=pagado_mes,
        num_pendientes=len(pendientes),
    )


@finanzas.route('/pago-proveedores/<int:id>/pagar', methods=['POST'])
@login_required
def pagar_orden(id):
    orden = OrdenCompra.query.get_or_404(id)

    if orden.PagoProveedor == 'Pagado':
        flash('Esta orden ya está pagada.', 'warning')
        return redirect(url_for('finanzas.pago_proveedores'))

    metodo = (request.form.get('metodo_pago') or '').strip()
    if metodo not in ('Efectivo', 'Transferencia'):
        flash('Selecciona un método de pago válido (Efectivo o Transferencia).', 'danger')
        return redirect(url_for('finanzas.pago_proveedores'))

    orden.PagoProveedor = 'Pagado'
    orden.metodoPago    = metodo
    orden.fechaPago     = datetime.now()
    db.session.commit()

    flash(f'Orden {orden.numeroLote} pagada por {metodo}.', 'success')
    return redirect(url_for('finanzas.pago_proveedores'))
