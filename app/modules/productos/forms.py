from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class ProductoForm(FlaskForm):
    NombreProducto = StringField(
        'Nombre del producto',
        validators=[
            DataRequired(message='El nombre es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    DescripcionProducto = TextAreaField(
        'Descripción',
        validators=[
            Optional(),
            Length(max=500, message='Máximo 500 caracteres.')
        ]
    )
    PrecioCompraProducto = FloatField(
        'Precio de compra',
        validators=[
            DataRequired(message='Ingresa el precio de compra.'),
            NumberRange(min=0, message='El precio no puede ser negativo.')
        ]
    )
    PrecioVentaProducto = FloatField(
        'Precio de venta',
        validators=[
            DataRequired(message='Ingresa el precio de venta.'),
            NumberRange(min=0, message='El precio no puede ser negativo.')
        ]
    )
    idCategoria = SelectField(
        'Categoría',
        coerce=int,
        validators=[Optional()]
    )
    foto = FileField(
        'Foto del producto',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo imágenes JPG, PNG o WEBP.')
        ]
    )
