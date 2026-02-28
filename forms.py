from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

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

class ComprasForm(FlaskForm):
    proveedor = StringField(
        'Proveedor',
        validators= [
            DataRequired(message='El proveedor es obligatorio'),
        ]
    )

class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=50)])
    # Regex para cumplir estrictamente con el requerimiento A07 
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message="La contraseña no cumple con la política de seguridad requerida.")
    ])
    id_rol = SelectField('Rol', coerce=int, validators=[DataRequired()])
    estatus = BooleanField('Activo', default=True)