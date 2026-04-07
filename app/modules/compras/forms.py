from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, DateField
from wtforms.validators import DataRequired, Optional


class OrdenCompraForm(FlaskForm):
    """
    Valida los campos estáticos del encabezado de la orden.
    Los renglones dinámicos (materia_proveida_id[], cantidades, precios)
    se validan manualmente en la ruta porque son arrays de longitud variable.
    """
    proveedor_id = IntegerField(
        'Proveedor',
        validators=[DataRequired(message='Debes seleccionar un proveedor.')]
    )
