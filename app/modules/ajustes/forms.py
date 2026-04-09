from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

# 🔹 RESTORE (.sql)
class RestoreForm(FlaskForm):
    file = FileField(
        "Archivo SQL",
        validators=[
            FileRequired(message="Debes subir un archivo"),
            FileAllowed(["sql"], "Solo archivos .sql")
        ]
    )
    submit = SubmitField("Restaurar")


# 🔹 IMPORT (.csv)
class ImportForm(FlaskForm):
    tabla = SelectField(
        "Tabla",
        choices=[
            ('user', 'user'),
            ('producto', 'producto'),
            ('categoria', 'categoria'),
            ('conversor', 'conversor'),
            ('unidad_medida', 'unidad_medida'),
            ('corte', 'corte')
        ],
        validators=[DataRequired()]
    )

    file = FileField(
        "Archivo CSV",
        validators=[
            FileRequired(message="Debes subir un archivo"),
            FileAllowed(["csv"], "Solo archivos CSV")
        ]
    )

    submit = SubmitField("Importar")