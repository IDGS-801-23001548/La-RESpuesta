from flask import render_template, redirect, url_for, flash, request
from . import produccion
from app.extensions import db, mongo_fotos
from app.models import (
    SolicitudProduccion, SolicitudProduccionDetalle,
    Lote, CanalCorte, Canal, Corte, Categoria,
)
from flask_login import login_required, current_user
from flask_security import roles_required
from datetime import datetime, date



# ═════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _foto_b64_de(id_foto):
    """Foto desde MongoDB en base64."""
    if not id_foto or mongo_fotos is None:
        return None
    try:
        doc = mongo_fotos.find_one({'idFoto': str(id_foto)})
        if doc and doc.get('foto'):
            raw = doc['foto']
            if not raw.startswith('data:'):
                raw = f'data:image/jpeg;base64,{raw}'
            return raw
    except Exception:
        pass
    return None


def _generar_numero_lote_produccion():
    """Numero de lote para Lote producido por corte.
    Formato: LP-MesDDNN  (ej: LP-Abr0901)."""
    meses_corto = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',
                   7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
    hoy = date.today()
    prefijo = f"LP-{meses_corto[hoy.month]}{hoy.day:02d}"
    ultimo = (
        Lote.query
        .filter(Lote.numeroLote.like(f"{prefijo}%"))
        .order_by(Lote.numeroLote.desc())
        .first()
    )
    if ultimo and ultimo.numeroLote:
        try:
            ultimo_num = int(ultimo.numeroLote[len(prefijo):])
        except (ValueError, IndexError):
            ultimo_num = 0
    else:
        ultimo_num = 0
    return f"{prefijo}{ultimo_num + 1:02d}"


# ═════════════════════════════════════════════════════════════════════════════
#  LISTADO — solicitudes pendientes de completar
# ═════════════════════════════════════════════════════════════════════════════

@produccion.route('/produccion')
@login_required
@roles_required('admin')
def index():
    pendientes = (
        SolicitudProduccion.query
        .filter(SolicitudProduccion.estatus == 'Pendiente')
        .order_by(SolicitudProduccion.fechaSolicitud.asc())
        .all()
    )

    completadas = (
        SolicitudProduccion.query
        .filter(SolicitudProduccion.estatus == 'Completada')
        .order_by(SolicitudProduccion.fechaCompletada.desc())
        .limit(20)
        .all()
    )

    # Enriquecer pendientes con datos del canal_corte
    items_pendientes = []
    for sol in pendientes:
        detalle = sol.detalles.first()
        cc = CanalCorte.query.get(detalle.idCanalCorte) if detalle and detalle.idCanalCorte else None
        corte = Corte.query.get(cc.idCorte) if cc else (sol.corte if sol.corte else None)
        canal = Canal.query.get(cc.idCanal) if cc else None
        cat = corte.categoria if corte and corte.categoria else None

        items_pendientes.append({
            'solicitud':        sol,
            'corte_nombre':     corte.nombreCorte if corte else '—',
            'categoria':        cat.nombreCategoria if cat else '—',
            'canal_id':         canal.idCanal if canal else '—',
            'canal_peso':       canal.Peso if canal else '—',
            'cantidad_esperada': cc.CantidadEsperada if cc else '—',
            'foto_b64':         _foto_b64_de(corte.idFoto) if corte else None,
        })

    # Enriquecer completadas
    items_completadas = []
    for sol in completadas:
        detalle = sol.detalles.first()
        lote_prod = Lote.query.get(detalle.idLoteProducido) if detalle and detalle.idLoteProducido else None
        cc = CanalCorte.query.get(detalle.idCanalCorte) if detalle and detalle.idCanalCorte else None
        corte = sol.corte

        items_completadas.append({
            'solicitud':     sol,
            'nombre':        sol.nombreReceta,
            'lote_numero':   lote_prod.numeroLote if lote_prod else '—',
            'kg_producidos': lote_prod.totalMateria if lote_prod else 0,
            'merma':         cc.Merma if cc else 0,
        })

    return render_template(
        'admin/produccion/produccion.html',
        items_pendientes=items_pendientes,
        items_completadas=items_completadas,
        total_pendientes=len(items_pendientes),
        total_completadas=len(items_completadas),
    )


# ═════════════════════════════════════════════════════════════════════════════
#  COMPLETAR — formulario para dar peso obtenido y concretar
# ═════════════════════════════════════════════════════════════════════════════

@produccion.route('/produccion/<int:id>/completar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def completar(id):
    sol = SolicitudProduccion.query.get_or_404(id)

    if sol.estatus != 'Pendiente':
        flash('Esta solicitud ya fue completada o cancelada.', 'warning')
        return redirect(url_for('produccion.index'))

    detalle = sol.detalles.first()
    cc = CanalCorte.query.get(detalle.idCanalCorte) if detalle and detalle.idCanalCorte else None
    corte = Corte.query.get(cc.idCorte) if cc else (sol.corte if sol.corte else None)
    canal = Canal.query.get(cc.idCanal) if cc else None
    cat = corte.categoria if corte and corte.categoria else None

    info = {
        'corte_nombre':     corte.nombreCorte if corte else '—',
        'categoria':        cat.nombreCategoria if cat else '—',
        'canal_id':         canal.idCanal if canal else '—',
        'canal_peso':       canal.Peso if canal else '—',
        'cantidad_esperada': cc.CantidadEsperada if cc else 0,
        'foto_b64':         _foto_b64_de(corte.idFoto) if corte else None,
        'fecha_sacrificio': canal.fechaSacrificio.strftime('%d/%m/%Y') if (canal and canal.fechaSacrificio) else '—',
    }

    if request.method == 'POST':
        try:
            cantidad_obtenida = float(request.form.get('cantidadObtenida') or 0)
        except (TypeError, ValueError):
            flash('La cantidad obtenida debe ser un numero valido.', 'danger')
            return redirect(url_for('produccion.completar', id=id))

        if cantidad_obtenida <= 0:
            flash('La cantidad obtenida debe ser mayor a cero.', 'danger')
            return redirect(url_for('produccion.completar', id=id))

        if not cc:
            flash('No se encontro el canal_corte vinculado a esta solicitud.', 'danger')
            return redirect(url_for('produccion.completar', id=id))

        try:
            esperada = cc.CantidadEsperada or 0
            merma    = round(esperada - cantidad_obtenida, 3)

            # 1) Marcar el canal_corte como Consumido
            cc.CantidadObtenida = cantidad_obtenida
            cc.Merma            = merma
            cc.estatus          = 'Consumido'

            # 2) Crear el Lote producido
            numero_lote = _generar_numero_lote_produccion()
            lote_producido = Lote(
                idCanalCorte      = cc.idCanalCorte,
                idMateriaProveida = None,
                idOrdenCompra     = None,
                numeroLote        = numero_lote,
                cantidadDeUnidad  = 1,
                cantidadPorUnidad = cantidad_obtenida,
                totalMateria      = cantidad_obtenida,
                precioPorUnidad   = 0.0,
                totalCosto        = 0.0,
                fechaCaducidad    = None,
                estatus           = 'Disponible',
                idUsuario         = current_user.id
            )
            db.session.add(lote_producido)
            db.session.flush()

            # 3) Completar la solicitud
            sol.estatus         = 'Completada'
            sol.fechaCompletada = datetime.now()

            # 4) Actualizar el detalle con el lote producido y la cantidad
            if detalle:
                detalle.idLoteProducido   = lote_producido.idLote
                detalle.cantidadConsumida = cantidad_obtenida

            db.session.commit()

            cat_nombre = cat.nombreCategoria if cat else ''
            nombre_corte = f'{corte.nombreCorte} ({cat_nombre})' if (corte and cat_nombre) else (corte.nombreCorte if corte else '—')
            flash(
                f'Produccion completada: "{nombre_corte}". '
                f'Lote {numero_lote} creado con {cantidad_obtenida:g} kg '
                f'(merma: {merma:g} kg).',
                'success'
            )
            return redirect(url_for('produccion.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al completar la produccion: {e}', 'danger')
            return redirect(url_for('produccion.completar', id=id))

    return render_template(
        'admin/produccion/produccion_completar.html',
        solicitud=sol,
        info=info,
    )
