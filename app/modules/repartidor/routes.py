from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import repartidor_bp
from app.extensions import db
from app.models import Pedido 

@repartidor_bp.route("/", methods=['GET'])
@login_required
def dashboard():
    return redirect(url_for("repartidor.pedidos"))

@repartidor_bp.route("/pedidos", methods=['GET'])
@login_required
def pedidos():
    id_repartidor_actual = current_user.id 
    pedidos_db = Pedido.query.filter_by(idRepartidor=id_repartidor_actual).all()
    
    # ---> NUEVO: Calculamos el efectivo acumulado para el modal <---
    total_efectivo_entregar = sum(p.Total for p in pedidos_db if p.Estatus == 'Finalizado' and p.Tipo == 'Efectivo')
    
    orden_estados = {'EnCurso': 1, 'Pendiente': 2, 'Finalizado': 3, 'Cancelado': 4}
    pedidos_db.sort(key=lambda p: orden_estados.get(p.Estatus, 5))
    
    return render_template("repartidor/pedidos.html", 
                           pedidos_db=pedidos_db, 
                           total_efectivo=total_efectivo_entregar)

@repartidor_bp.route("/pedido/<int:id_pedido>", methods=['GET'])
@login_required
def detalle_pedido(id_pedido):
    # Buscamos el pedido, si no existe lanza 404
    pedido_db = Pedido.query.get_or_404(id_pedido)
    
    # Verificamos que el pedido SI sea de Isaac (seguridad básica)
    if pedido_db.idRepartidor != current_user.id:
        flash("No tienes permiso para ver este pedido.", "error")
        return redirect(url_for("repartidor.pedidos"))
        
    # Checamos si hay ALGÚN pedido en curso para saber si bloquear el botón de "Iniciar"
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
    
    # Bloqueo de un solo viaje a la vez
    if nuevo_estado == 'EnCurso':
        viaje_activo = Pedido.query.filter_by(idRepartidor=current_user.id, Estatus='EnCurso').first()
        if viaje_activo:
            flash("Ya tienes un pedido en curso.", "warning")
            return redirect(url_for('repartidor.detalle_pedido', id_pedido=id_pedido))

    if nuevo_estado:
        pedido_db.Estatus = nuevo_estado
        # Si es cancelación, guardamos el motivo en la columna "Notas" (que ya existe)
        if nuevo_estado == 'Cancelado':
            motivo = request.form.get('motivo_cancelacion')
            pedido_db.Notas = f"MOTIVO CANCELACIÓN: {motivo}"
        
        db.session.commit()
        flash(f"Estado actualizado", "success")
        
    # AQUÍ ESTÁ EL CAMBIO: Te quedas en la misma pantalla en lugar de ir a la lista
    return redirect(url_for('repartidor.detalle_pedido', id_pedido=id_pedido))

@repartidor_bp.route("/entregar_pedido/<int:id_pedido>", methods=['POST'])
@login_required
def entregar_pedido(id_pedido):
    pedido_db = Pedido.query.get_or_404(id_pedido)
    
    # Validación de seguridad
    if pedido_db.idRepartidor != current_user.id:
        flash("No tienes permiso para modificar este pedido.", "error")
        return redirect(url_for("repartidor.pedidos"))
        
    # Cambiamos a Finalizado (como lo tienen tus compañeros)
    pedido_db.Estatus = 'Finalizado'
    db.session.commit()
    
    return redirect(url_for("repartidor.pedidos"))


@repartidor_bp.route("/cerrar-ruta")
@login_required
def cerrar_ruta():
    # 1. BUSCAR CUALQUIER PEDIDO QUE NO ESTÉ NI ENTREGADO NI CANCELADO
    # Buscamos 'Pendiente' o 'EnCurso'. Si existe aunque sea uno, Isaac no se va.
    pedido_abierto = Pedido.query.filter(
        Pedido.idRepartidor == current_user.id,
        Pedido.Estatus.in_(['Pendiente', 'EnCurso'])
    ).first()
    
    if pedido_abierto:
        # Si encuentra uno, le mandamos el mensaje de error y lo regresamos
        flash("¡DENEGADO! No puedes finalizar jornada. Tienes pedidos pendientes o en curso que debes entregar o cancelar.", "error")
        return redirect(url_for('repartidor.pedidos'))

    # 2. CALCULAR EL EFECTIVO (Solo los que sí entregó y eran cash)
    pedidos_del_dia = Pedido.query.filter_by(
        idRepartidor=current_user.id, 
        Estatus='Finalizado', 
        Tipo='Efectivo'
    ).all()
    
    total_efectivo = sum(p.Total for p in pedidos_del_dia)

    # 3. LIMPIEZA DEL DASHBOARD
    # Desvinculamos al repartidor de sus pedidos finalizados para que mañana empiece de cero
    for p in Pedido.query.filter_by(idRepartidor=current_user.id).all():
        p.idRepartidor = None 
    
    db.session.commit()

    # 4. LOGOUT TÉCNICO (Sin mensaje de flash para que sea limpio, como pediste)
    from flask_login import logout_user
    logout_user()
    
    # Solo mandamos el mensaje de la liquidación de caja al login
    flash(f"Ruta finalizada. Entrega ${total_efectivo:.2f} en caja.", "success")
    return redirect(url_for('auth.login'))