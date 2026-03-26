from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


PASSWORD_REGEX = (
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)'
    r'(?=.*[!@#$%^&*()\-_=+\[\]{};:\'",.<>/?\\|`~])'
    r'[A-Za-z\d!@#$%^&*()\-_=+\[\]{};:\'",.<>/?\\|`~]{8,}$'
)


class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message="El nombre de usuario es obligatorio."),
        Length(min=4, max=50, message="Debe tener entre 4 y 50 caracteres.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=8, message="Debe tener al menos 8 caracteres."),
        Regexp(PASSWORD_REGEX,
               message="La contraseña debe tener mayúscula, minúscula, número y carácter especial.")
    ])
    id_rol = SelectField('Rol', coerce=int, validators=[
        DataRequired(message="Selecciona un rol.")
    ])
    estatus = BooleanField('Activo', default=True)