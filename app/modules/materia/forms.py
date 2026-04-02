from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, SelectMultipleField,
    TextAreaField, RadioField, DecimalField, widgets
)
from wtforms.validators import DataRequired, Optional, Length, NumberRange, ValidationError


UNIDADES_COMPRA = [
    ('',           'Seleccionar...'),
    ('canal',      'Canal entera'),
    ('media_canal','Media canal'),
    ('pieza',      'Pieza'),
    ('kg',         'Kilogramo (kg)'),
    ('ton',        'Tonelada (ton)'),
    ('litro',      'Litro (L)'),
    ('bulto',      'Bulto'),
    ('caja',       'Caja'),
    ('bolsa',      'Bolsa'),
    ('paquete',    'Paquete'),
]


class MateriaPrimaForm(FlaskForm):

    nombre = StringField(
        'Nombre',
        validators=[DataRequired(message='El nombre es obligatorio.'), Length(max=100)]
    )

    descripcion = TextAreaField(
        'Descripción',
        validators=[Optional()]
    )

    categoria = RadioField(
        'Categoría',
        choices=[('Canal', 'Canal'), ('Insumo', 'Insumo'), ('Reventa', 'Reventa')],
        default='Canal',
        validators=[DataRequired(message='Selecciona una categoría.')]
    )

    unidad_compra = SelectField(
        'Unidad de compra',
        choices=UNIDADES_COMPRA,
        validators=[DataRequired(message='Selecciona la unidad de compra.')]
    )

    unidad_estandar = SelectField(
        'Unidad estándar',
        choices=[
            ('g',   'Gramos (g)'),
            ('ml',  'Mililitros (mL)'),
            ('pza', 'Piezas (pza)'),
        ],
        default='g',
        validators=[DataRequired()]
    )

    # Cuántas unidades estándar equivale 1 unidad de compra.
    # No aplica para Reventa — se limpia en la ruta.
    factor_conversion = DecimalField(
        'Factor de conversión',
        validators=[Optional()],
        places=4
    )

    # Tipos de merma seleccionados (se guardan como CSV en el modelo)
    tipo_merma = SelectMultipleField(
        'Tipo de merma',
        choices=[
            ('produccion',  'Por producción / desposte'),
            ('manejo',      'Por manejo / almacenamiento'),
            ('desperdicio', 'Por desperdicio general'),
        ],
        validators=[Optional()],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )

    pct_merma = DecimalField(
        '% de merma',
        validators=[
            Optional(),
            NumberRange(min=0, max=100, message='La merma debe estar entre 0 y 100.')
        ],
        places=2,
        default=0
    )

    # En unidad estándar
    stock_minimo = DecimalField(
        'Stock mínimo',
        validators=[
            DataRequired(message='Define el stock mínimo de alerta.'),
            NumberRange(min=0, message='El stock mínimo no puede ser negativo.')
        ],
        places=4,
        default=0
    )

    # Costo por unidad estándar; se recalcula automáticamente con cada compra
    costo_promedio = DecimalField(
        'Costo promedio inicial',
        validators=[
            Optional(),
            NumberRange(min=0, message='El costo no puede ser negativo.')
        ],
        places=4,
        default=0
    )

    def validate_factor_conversion(self, field):
        """Canal e Insumo requieren factor de conversión mayor que cero."""
        if self.categoria.data in ('Canal', 'Insumo'):
            if field.data is None or field.data <= 0:
                raise ValidationError(
                    'El factor de conversión es obligatorio para Canal e Insumo.'
                )
