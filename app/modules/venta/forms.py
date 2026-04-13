# app/modules/venta/forms.py

from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class AgregarAlCarritoForm(FlaskForm):
    """
    Formulario CSRF mínimo para agregar una unidad de un producto al carrito.
    Se usa en las tarjetas del catálogo, en carrito.html y en pedido_detalle.html.

    Uso en template:
        <form method="POST" action="{{ url_for('venta.agregar_al_carrito', id_producto=p.idProducto) }}">
            {{ form.hidden_tag() }}
            <button type="submit">Agregar</button>
        </form>

    Uso en routes:
        from app.modules.venta.forms import AgregarAlCarritoForm
        form = AgregarAlCarritoForm()
        if form.validate_on_submit():
            ...
    """
    # Sin campos adicionales: solo necesitamos el token CSRF que provee hidden_tag().
    # Si en el futuro se necesita elegir cantidad, se puede agregar:
    # cantidad = IntegerField('Cantidad', default=1, validators=[NumberRange(min=1)])
    pass
