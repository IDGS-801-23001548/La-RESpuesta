from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[
            DataRequired(message='El usuario es obligatorio.'),
            Length(min=3, max=80, message='Mínimo 3 caracteres.')
        ]
    )
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message='La contraseña es obligatoria.'),
            Length(min=4, message='Mínimo 4 caracteres.')
        ]
    )
    remember = BooleanField('Recordarme')
    submit   = SubmitField('Ingresar')