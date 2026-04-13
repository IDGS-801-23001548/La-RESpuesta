from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, TelField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, Optional

# Regex de contraseña segura
PASSWORD_REGEX = (
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)'
    r'(?=.*[!@#$%^&*()\-_=+\[\]{};:\'",.<>/?\\|`~])'
    r'[A-Za-z\d!@#$%^&*()\-_=+\[\]{};:\'",.<>/?\\|`~]{8,}$'
)


class UserForm(FlaskForm):
    """Formulario para administración de usuarios (panel interno)."""

    # PERSONA
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido_paterno = StringField('Apellido paterno', validators=[DataRequired(), Length(max=100)])
    apellido_materno = StringField('Apellido materno', validators=[DataRequired(), Length(max=100)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=255)])

    # USUARIO
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Regexp(PASSWORD_REGEX, message="La contraseña debe tener mayúscula, minúscula, número y símbolo.")
        ]
    )

    id_rol = SelectField('Rol', coerce=int, validators=[DataRequired()])
    active = BooleanField('Activo', default=True)


class RegistroClienteForm(FlaskForm):
    """Formulario de registro público para clientes."""

    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message='El nombre es obligatorio.'),
            Length(max=100)
        ])

    apellido_paterno = StringField(
        'Apellido paterno',
        validators=[
            DataRequired(message='El apellido paterno es obligatorio.'),
            Length(max=100)
        ])

    apellido_materno = StringField(
        'Apellido materno',
        validators=[
            Optional(),
            Length(max=100)
        ])

    telefono = TelField(
        'Teléfono',
        validators=[
            Optional(),
            Length(max=20)
        ])

    direccion = StringField(
        'Dirección de entrega',
        validators=[
            Optional(),
            Length(max=255)
        ])

    email = StringField(
        'Correo electrónico',
        validators=[
            DataRequired(message='El correo es obligatorio.'),
            Email(message='Ingresa un correo válido.'),
            Length(max=100)
        ])

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message='La contraseña es obligatoria.'),
            Length(min=8, message='Mínimo 8 caracteres.')
        ])

    password_confirm = PasswordField(
        'Confirmar contraseña',
        validators=[
            DataRequired(message='Confirma tu contraseña.'),
            EqualTo('password', message='Las contraseñas no coinciden.')
        ])