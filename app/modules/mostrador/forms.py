from flask_wtf import FlaskForm
from wtforms import FloatField, HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class AgregarProductoForm(FlaskForm):
    cantidad = IntegerField(
        'Cantidad',
        default=1,
        validators=[
            DataRequired(message='La cantidad es requerida.'),
            NumberRange(min=1, message='La cantidad debe ser mayor a 1'),
        ]
    )
    submit = SubmitField('Agregar')


class AgregarCorteForm(FlaskForm):
    """Formulario para agregar un corte al carrito por peso (kg)."""
    peso = FloatField(
        'Peso (kg)',
        default=0.5,
        validators=[
            DataRequired(message='El peso es requerido.'),
            NumberRange(min=0.1, message='El peso mínimo es 0.1 kg.'),
        ]
    )
    submit = SubmitField('Agregar')


class ModificarCantidadForm(FlaskForm):
    cantidad = FloatField(
        'Cantidad',
        validators=[
            DataRequired(message='La cantidad es requerida.'),
            NumberRange(min=0, message='La cantidad no puede ser negativa.'),
        ]
    )


class EliminarProductoForm(FlaskForm):
    pass


class VaciarCarritoForm(FlaskForm):
    pass


class CobrarForm(FlaskForm):
    """
    tipo_pago  : 'Efectivo' | 'Tarjeta'   — enviado desde el modal
    referencia : número de autorización de tarjeta (opcional)
    """
    tipo_pago  = HiddenField('Tipo de pago',  default='Efectivo')
    referencia = HiddenField('Referencia',    default='')


class EntregarPedidoForm(FlaskForm):
    """
    Confirmar entrega de un pedido.
    tipo_pago y referencia son opcionales: solo se envían cuando el pedido
    estaba pendiente de cobro y se paga en el modal antes de entregar.
    """
    tipo_pago  = HiddenField('Tipo de pago',  default='')
    referencia = HiddenField('Referencia',    default='')