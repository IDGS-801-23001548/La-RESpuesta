from flask import Flask, render_template, request, redirect, url_for
from forms import LoginForm, ComprasForm

app = Flask(__name__)
app.secret_key = 'clave-temporal-cambiar-en-produccion'

# Hace que 'current_endpoint' esté disponible en TODOS los templates
# sin necesidad de pasarlo manualmente en cada route
@app.context_processor
def inject_current_endpoint():
    return {'current_endpoint': request.endpoint}

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/admin' , methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')

@app.route('/pos')
def pos():
    return render_template('pos/pos.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# ─────────────────────────────────────────
# Rutas placeholder — solo vista por ahora
# Cuando implementes cada módulo reemplaza
# render_template('admin/admin.html') por
# su propio template
# ─────────────────────────────────────────

@app.route('/compras')
def compras():
    return render_template('admin/compras.html')

@app.route('/compras/nueva', methods=['GET', 'POST'])
def compras_nueva():
    form = ComprasForm()   # cuando implementes el form
    return render_template('admin/compras_nueva.html', form=form)

@app.route('/compras/<int:id>')
def compras_detalle(id):
    return render_template('admin/compras_detalle.html')

@app.route('/materia')
def materia():
    return render_template('admin/admin.html')

@app.route('/recetas')
def recetas():
    return render_template('admin/admin.html')

@app.route('/produccion')
def produccion():
    return render_template('admin/admin.html')

@app.route('/solicitudes')
def solicitudes():
    return render_template('admin/admin.html')

@app.route('/productos')
def productos():
    return render_template('admin/admin.html')

@app.route('/ventas')
def ventas():
    return render_template('admin/admin.html')

@app.route('/pagoProveedores')
def pagoProveedores():
    return render_template('admin/admin.html')

@app.route('/corteDiario')
def corteDiario():
    return render_template('admin/admin.html')

@app.route('/utilidad')
def utilidad():
    return render_template('admin/admin.html')

@app.route('/reportes')
def reportes():
    return render_template('admin/admin.html')

@app.route('/usuarios')
def usuarios():
    return render_template('admin/admin.html')

@app.route('/logs')
def logs():
    return render_template('admin/admin.html')


if __name__ == '__main__':
    app.run(debug=True)