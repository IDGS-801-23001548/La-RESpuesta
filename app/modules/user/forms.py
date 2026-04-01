from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, Email

PASSWORD_REGEX = (
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)'
    r'(?=.*[!@#$%^&*()\-_=+\[\]{};:\'",.<>/?\\|`~])'
    r'[A-Za-z\d!@#$%^&*()\-_=+\[\]{};:\'",.<>/?\\|`~]{8,}$'
)

class UserForm(FlaskForm):
    # PERSONA
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido_paterno = StringField('Apellido', validators=[DataRequired()])
    apellido_materno = StringField('Apellido', validators=[DataRequired()])
    telefono = StringField('Teléfono')
    direccion = StringField('Dirección')

    # USUARIO
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    id_rol = SelectField('Rol', coerce=int, validators=[DataRequired()])
    active = BooleanField('Activo', default=True)