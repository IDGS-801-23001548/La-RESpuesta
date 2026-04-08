from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


class RecetaForm(FlaskForm):
    """Datos basicos de una receta. Las materias primas y cantidades
    se reciben aparte como listas en el request (ingrediente_id[], ingrediente_cantidad[])."""

    idProducto = SelectField(
        'Producto a producir',
        coerce=int,
        validators=[DataRequired(message='Debes seleccionar un producto.')]
    )
    descripcion = TextAreaField(
        'Descripcion',
        validators=[Optional(), Length(max=500, message='Maximo 500 caracteres.')]
    )
