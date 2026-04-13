from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from . import repartidor_bp
from app.extensions import db
from app.models import Pedido 
import logging

# Configuramos el logger para que escriba en app.log con el formato de tus compas
logger = logging.getLogger('app')

@repartidor_bp.route("/", methods=['GET'])
@login_required
def dashboard():
    return redirect(url_for("repartidor.pedidos"))

@repartidor_bp.route("/pedidos", methods=['GET'])
@login_required
def pedidos():
    id_repartidor_actual = current_user.id 
    pedidos_db = Pedido.query.filter_by(idRepartidor=id_repartidor_actual).all()
    
    total_efectivo_entregar = sum(p.Total for p in pedidos_db if p.Estatus == 'Finalizado' and p.Tipo == 'Efectivo')
    
    orden_estados = {'EnCurso': 1, 'Pendiente': 2, 'Finalizado': 3, 'Cancelado': 4}
    pedidos_db.sort(key=lambda p: orden_estados.get(p.Estatus, 5))
    
    return render_template("repartidor/pedidos.html", 
                           pedidos_db=pedidos_db, 
                           total_efectivo=total_efectivo_entregar)

@repartidor_bp.route("/pedido/<int:id_pedido>", methods=['GET'])
@login_required
def detalle_pedido(id_pedido):
    pedido_db = Pedido.query.get_or_404(id_pedido)
    
    if pedido_db.idRepartidor != current_user.id:
        flash("No tienes permiso para ver este pedido.", "error")
        return redirect(url_for("repartidor.pedidos"))
        
    viaje_activo = Pedido.query.filter_by(idRepartidor=current_user.id, Estatus='EnCurso').first()
    tiene_viaje_activo = True if viaje_activo else False
        
    return render_template("repartidor/detalle.html", 
                           pedido=pedido_db, 
                           tiene_viaje_activo=tiene_viaje_activo)

@repartidor_bp.route("/actualizar_estado/<int:id_pedido>", methods=['POST'])
@login_required
def actualizar_estado(id_pedido):
    pedido_db = Pedido.query.get_or_404(id_pedido)
    nuevo_estado = request.form.get('estado')
    
    if nuevo_estado == 'EnCurso':
        viaje_activo = Pedido.query.filter_by(idRepartidor=current_user.id, Estatus='EnCurso').first()
        if viaje_activo:
            flash("Ya tienes un pedido en curso.", "warning")
            return redirect(url_for('repartidor.detalle_pedido', id_pedido=id_pedido))
        # LOG DE INICIO DE VIAJE
        logger.info(f"VIAJE INICIADO - Repartidor: {current_user.name} - Pedido: #{id_pedido}")

    if nuevo_estado:
        pedido_db.Estatus = nuevo_estado
        if nuevo_estado == 'Cancelado':
            motivo = request.form.get('motivo_cancelacion')
            pedido_db.Notas = f"MOTIVO CANCELACIÓN: {motivo}"
            # LOG DE CANCELACIÓN
            logger.warning(f"CANCELACION SOLICITADA - Pedido: #{id_pedido} - Motivo: {motivo}")
        
        db.session.commit()
        flash(f"Estado actualizado", "success")
        
    return redirect(url_for('repartidor.detalle_pedido', id_pedido=id_pedido))

@repartidor_bp.route("/entregar_pedido/<int:id_pedido>", methods=['POST'])
@login_required
def entregar_pedido(id_pedido):
    pedido_db = Pedido.query.get_or_404(id_pedido)
    
    if pedido_db.idRepartidor != current_user.id:
        flash("No tienes permiso para modificar este pedido.", "error")
        return redirect(url_for("repartidor.pedidos"))
        
    pedido_db.Estatus = 'Finalizado'
    db.session.commit()
    
    # LOG DE ENTREGA EXITOSA
    logger.info(f"PEDIDO ENTREGADO - Repartidor: {current_user.name} - Pedido: #{id_pedido} - Total: ${pedido_db.Total}")
    
    return redirect(url_for("repartidor.pedidos"))

@repartidor_bp.route("/cerrar-ruta")
@login_required
def cerrar_ruta():
    # Candado: No dejar salir si hay algo pendiente
    pedido_abierto = Pedido.query.filter(
        Pedido.idRepartidor == current_user.id,
        Pedido.Estatus.in_(['Pendiente', 'EnCurso'])
    ).first()
    
    if pedido_abierto:
        return redirect(url_for('repartidor.pedidos'))

    # Cálculo de efectivo para el log y el mensaje
    pedidos_del_dia = Pedido.query.filter_by(
        idRepartidor=current_user.id, 
        Estatus='Finalizado', 
        Tipo='Efectivo'
    ).all()
    
    total_efectivo = sum(p.Total for p in pedidos_del_dia)

    # Limpieza del dashboard (desvincular pedidos)
    for p in Pedido.query.filter_by(idRepartidor=current_user.id).all():
        p.idRepartidor = None 
    
    db.session.commit()

    # LOG DE CIERRE DE JORNADA
    logger.info(f"JORNADA FINALIZADA - Repartidor: {current_user.name} - Efectivo entregado: ${total_efectivo:.2f}")

    logout_user()
    
    flash(f"Ruta finalizada. Entrega ${total_efectivo:.2f} en caja.", "success")
    return redirect(url_for('auth.login'))