from flask_wtf import FlaskForm


class OrdenCompraForm(FlaskForm):
    """Solo necesitamos el token CSRF; el resto se valida en la ruta."""
    pass
