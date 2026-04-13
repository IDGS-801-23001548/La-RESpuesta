from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, SelectMultipleField,
    TextAreaField, RadioField, widgets
)
from wtforms.validators import DataRequired, Optional, Email, Length, Regexp


class ProveedorForm(FlaskForm):

    nombre = StringField(
        'Nombre / Razon social',
        validators=[DataRequired(), Length(max=150)]
    )

    rfc = StringField(
        'RFC',
        validators=[
            DataRequired(),
            Length(min=12, max=13),
            Regexp(r'^[A-Z0-9]{12,13}$', message='RFC invalido. Solo mayusculas y numeros, 12 o 13 caracteres.')
        ]
    )

    estatus = RadioField(
        'Estatus',
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')],
        default='activo',
        validators=[DataRequired()]
    )

    contacto = StringField(
        'Nombre del contacto',
        validators=[DataRequired(), Length(max=100)]
    )

    telefono = StringField(
        'Telefono',
        validators=[DataRequired(), Length(max=20)]
    )

    correo = StringField(
        'Correo electronico',
        validators=[Optional(), Email(), Length(max=120)]
    )

    direccion = StringField(
        'Direccion',
        validators=[Optional(), Length(max=250)]
    )

    condicion_pago = SelectField(
        'Condicion de pago',
        choices=[
            ('',           'Seleccionar...'),
            ('contado',    'Contado'),
            ('credito_8',  'Credito 8 dias'),
            ('credito_15', 'Credito 15 dias'),
            ('credito_30', 'Credito 30 dias'),
        ],
        validators=[DataRequired(message='Selecciona una condicion de pago.')]
    )

    dias_entrega = SelectMultipleField(
        'Dias de entrega',
        choices=[
            ('Lunes',      'Lunes'),
            ('Martes',     'Martes'),
            ('Miércoles',  'Miércoles'),
            ('Jueves',     'Jueves'),
            ('Viernes',    'Viernes'),
            ('Sábado',     'Sábado'),
            ('Domingo',    'Domingo'),
        ],
        validators=[Optional()],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )

    notas = TextAreaField(
        'Notas adicionales',
        validators=[Optional()]
    )
