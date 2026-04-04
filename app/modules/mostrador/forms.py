from flask_wtf import FlaskForm
from wtforms import FloatField, HiddenField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


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


class ModificarCantidadForm(FlaskForm):
    cantidad = IntegerField(
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
    pass