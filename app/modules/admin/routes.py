from datetime import datetime, timedelta, date
from flask import render_template, request
from flask_security import login_required, roles_required
from sqlalchemy import func

from app.extensions import db
from app.models import Pedido, ProductoUnitario, Producto
from app.models.vistaResumenPedido import VistaResumenPedido
from . import admin


@admin.route('/dashboard-ventas')
@login_required
@roles_required('admin')
def dashboard_ventas():

    # ── 1. Rango de fechas ──────────────────────────────────────────────
    preset = request.args.get('preset', 'hoy')
    hoy = date.today()

    if preset == 'hoy':
        desde = datetime.combine(hoy, datetime.min.time())
        hasta = datetime.combine(hoy, datetime.max.time())
    elif preset == 'semana':
        desde = datetime.combine(hoy - timedelta(days=hoy.weekday()), datetime.min.time())
        hasta = datetime.combine(hoy, datetime.max.time())
    elif preset == 'mes':
        desde = datetime.combine(hoy.replace(day=1), datetime.min.time())
        hasta = datetime.combine(hoy, datetime.max.time())
    else:
        # rango personalizado
        try:
            desde = datetime.strptime(request.args.get('desde', hoy.strftime('%Y-%m-%d')), '%Y-%m-%d')
            hasta = datetime.strptime(request.args.get('hasta', hoy.strftime('%Y-%m-%d')), '%Y-%m-%d')
            hasta = hasta.replace(hour=23, minute=59, second=59)
        except ValueError:
            desde = datetime.combine(hoy, datetime.min.time())
            hasta = datetime.combine(hoy, datetime.max.time())

    # ── 2. Consultas base sobre Pedido ──────────────────────────────────
    pedidos_q = Pedido.query.filter(
        Pedido.fechaCreacion >= desde,
        Pedido.fechaCreacion <= hasta,
    )

    pedidos_finalizados_q = pedidos_q.filter(Pedido.Estatus == 'Finalizado')

    total_pedidos        = pedidos_q.count()
    pedidos_finalizados  = pedidos_q.filter(Pedido.Estatus == 'Finalizado').count()
    pedidos_cancelados   = pedidos_q.filter(Pedido.Estatus == 'Cancelado').count()
    pedidos_en_curso     = pedidos_q.filter(Pedido.Estatus == 'EnCurso').count()

    # Monto total (solo finalizados)
    total_vendido = db.session.query(
        func.coalesce(func.sum(Pedido.Total), 0)
    ).filter(
        Pedido.fechaCreacion >= desde,
        Pedido.fechaCreacion <= hasta,
        Pedido.Estatus == 'Finalizado',
    ).scalar() or 0.0

    ticket_promedio = total_vendido / pedidos_finalizados if pedidos_finalizados > 0 else 0.0

    # ── 3. Cambio vs periodo anterior (mismo tamaño) ────────────────────
    delta      = hasta - desde
    desde_prev = desde - (delta + timedelta(seconds=1))
    hasta_prev = desde - timedelta(seconds=1)

    total_prev = db.session.query(
        func.coalesce(func.sum(Pedido.Total), 0)
    ).filter(
        Pedido.fechaCreacion >= desde_prev,
        Pedido.fechaCreacion <= hasta_prev,
        Pedido.Estatus == 'Finalizado',
    ).scalar() or 0.0

    if total_prev > 0:
        cambio_total = ((total_vendido - total_prev) / total_prev) * 100
    else:
        cambio_total = 100.0 if total_vendido > 0 else 0.0

    # ── 4. Tipo de pago ─────────────────────────────────────────────────
    def suma_por_tipo(tipo):
        return db.session.query(
            func.coalesce(func.sum(Pedido.Total), 0)
        ).filter(
            Pedido.fechaCreacion >= desde,
            Pedido.fechaCreacion <= hasta,
            Pedido.Estatus == 'Finalizado',
            Pedido.Tipo == tipo,
        ).scalar() or 0.0

    total_efectivo      = suma_por_tipo('Efectivo')
    total_tarjeta       = suma_por_tipo('Tarjeta')
    total_transferencia = suma_por_tipo('Transferencia')
    suma_pagos          = total_efectivo + total_tarjeta + total_transferencia

    def pct(val):
        return round(val / suma_pagos * 100, 1) if suma_pagos > 0 else 0

    pct_efectivo      = pct(total_efectivo)
    pct_tarjeta       = pct(total_tarjeta)
    pct_transferencia = pct(total_transferencia)

    # ── 5. Tipo de entrega ──────────────────────────────────────────────
    def count_entrega(tipo):
        return pedidos_q.filter(Pedido.Entrega == tipo).count()

    pedidos_mostrador = count_entrega('Mostrador')
    pedidos_domicilio = count_entrega('Domicilio')
    suma_entregas     = pedidos_mostrador + pedidos_domicilio

    pct_mostrador = round(pedidos_mostrador / suma_entregas * 100, 1) if suma_entregas > 0 else 0
    pct_domicilio = round(pedidos_domicilio / suma_entregas * 100, 1) if suma_entregas > 0 else 0

    # ── 6. Top productos vendidos (via VistaResumenPedido) ──────────────
    #  La vista ya agrega cantidad y subtotal por producto × pedido.
    #  Hacemos GROUP BY idProducto para obtener totales del periodo.
    top_productos_raw = db.session.query(
        VistaResumenPedido.NombreProducto,
        VistaResumenPedido.PrecioVentaProducto,
        func.sum(VistaResumenPedido.cantidad).label('cantidad'),
        func.sum(VistaResumenPedido.subtotal).label('subtotal'),
    ).join(
        Pedido, Pedido.idPedido == VistaResumenPedido.idPedido
    ).filter(
        Pedido.fechaCreacion >= desde,
        Pedido.fechaCreacion <= hasta,
        Pedido.Estatus == 'Finalizado',
    ).group_by(
        VistaResumenPedido.idProducto,
        VistaResumenPedido.NombreProducto,
        VistaResumenPedido.PrecioVentaProducto,
    ).order_by(
        func.sum(VistaResumenPedido.cantidad).desc()
    ).limit(8).all()

    # Convertimos a dicts para pasar fácilmente al template
    top_productos = [
        {
            'NombreProducto': r.NombreProducto,
            'PrecioVentaProducto': r.PrecioVentaProducto,
            'cantidad': r.cantidad,
            'subtotal': r.subtotal,
        }
        for r in top_productos_raw
    ]

    # ── 7. Presentaciones más vendidas (por categoría de producto) ──────
    #  Usamos Producto.NombreProducto como proxy de "presentación".
    #  Si tienes un modelo Corte puedes hacer el JOIN aquí.
    #  Por ahora agrupamos por categoría del producto.
    from app.models.categoria import Categoria   # importa tu modelo

    presentaciones_raw = db.session.query(
        Categoria.nombreCategoria.label('nombre'),
        func.sum(VistaResumenPedido.cantidad).label('cantidad'),
    ).join(
        Producto, Producto.idCategoria == Categoria.idCategoria
    ).join(
        VistaResumenPedido, VistaResumenPedido.idProducto == Producto.idProducto
    ).join(
        Pedido, Pedido.idPedido == VistaResumenPedido.idPedido
    ).filter(
        Pedido.fechaCreacion >= desde,
        Pedido.fechaCreacion <= hasta,
        Pedido.Estatus == 'Finalizado',
    ).group_by(
        Categoria.idCategoria, Categoria.nombreCategoria
    ).order_by(
        func.sum(VistaResumenPedido.cantidad).desc()
    ).limit(6).all()

    presentaciones = [
        {'nombre': r.nombre, 'cantidad': int(r.cantidad)}
        for r in presentaciones_raw
    ]

    # ── 8. Últimos pedidos del periodo ──────────────────────────────────
    ultimos_pedidos = pedidos_q.order_by(Pedido.fechaCreacion.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        # fechas
        desde=desde,
        hasta=hasta,
        preset=preset,
        # KPIs principales
        total_vendido=total_vendido,
        total_pedidos=total_pedidos,
        pedidos_finalizados=pedidos_finalizados,
        pedidos_cancelados=pedidos_cancelados,
        pedidos_en_curso=pedidos_en_curso,
        ticket_promedio=ticket_promedio,
        cambio_total=cambio_total,
        # pago
        total_efectivo=total_efectivo,
        total_tarjeta=total_tarjeta,
        total_transferencia=total_transferencia,
        pct_efectivo=pct_efectivo,
        pct_tarjeta=pct_tarjeta,
        pct_transferencia=pct_transferencia,
        # entrega
        pedidos_mostrador=pedidos_mostrador,
        pedidos_domicilio=pedidos_domicilio,
        pct_mostrador=pct_mostrador,
        pct_domicilio=pct_domicilio,
        # productos y presentaciones
        top_productos=top_productos,
        presentaciones=presentaciones,
        # tabla de últimos pedidos
        ultimos_pedidos=ultimos_pedidos,
        # utilidades de Jinja
        enumerate=enumerate,
    )