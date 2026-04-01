from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ComprasForm(FlaskForm):
    proveedor = StringField('Proveedor', validators=[
        DataRequired(message='El proveedor es obligatorio'),
    ])