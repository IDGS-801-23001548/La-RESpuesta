from flask_wtf import FlaskForm
from wtforms import FloatField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class AgregarProductoForm(FlaskForm):
    cantidad = FloatField(
        'Cantidad',
        default=1.0,
        validators=[
            DataRequired(message='La cantidad es requerida.'),
            NumberRange(min=0.001, message='La cantidad debe ser mayor a 0.'),
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