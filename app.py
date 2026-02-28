from flask import Flask, render_template, request, redirect, url_for, session, flash
from extensions import db
from config import DevelopmentConfig
from models import User, Role, Log
from forms import UserForm, LoginForm # Asegúrate de tener estos en forms.py
from datetime import datetime
from flask_wtf import FlaskForm, CSRFProtect

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
app.config['SECRET_KEY'] = 'your-secret-key'
csrf = CSRFProtect(app)

# --- UTILIDADES ---
def registrar_log(tipo, accion, descripcion, user_id=None):
    nuevo_log = Log(
        tipo_evento=tipo,
        accion=accion,
        descripcion=descripcion,
        id_usuario=user_id,
        ip_origen=request.remote_addr
    )
    db.session.add(nuevo_log)
    db.session.commit()

@app.context_processor
def inject_current_endpoint():
    return {'current_endpoint': request.endpoint}

# --- RUTAS DE ACCESO ---

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- RUTAS DE ADMINISTRACIÓN (Mapeadas al Sidebar) ---

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Endpoint: admin (Dashboard solicitado en RF01) """
    return render_template('admin/admin.html')

@app.route('/usuarios')
def usuarios():
    # Consulta mediante el ORM para evitar inyecciones SQL
    usuarios_db = User.query.all() 
    return render_template('admin/usuarios.html', usuarios_db=usuarios_db)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def usuarios_nuevo():
    form = UserForm()
    form.id_rol.choices = [(r.id_rol, r.nombre_rol) for r in Role.query.all()]
    
    if request.method == 'POST':
        nuevo_u = User(
            nombre_usuario=form.username.data,
            id_rol=form.id_rol.data
        )
        nuevo_u.set_password(form.password.data)
        nuevo_u.estatus = 'Activo' if form.estatus.data else 'Inactivo'
        
        db.session.add(nuevo_u)
        db.session.commit()

        registrar_log(
            tipo='Configuracion',
            accion='CREAR_USUARIO',
            descripcion=f"Usuario '{nuevo_u.nombre_usuario}' creado con rol ID {nuevo_u.id_rol}",
            user_id=session.get('user_id')
        )

        return redirect(url_for('usuarios'))
        
    return render_template('admin/usuarios_nuevo.html', form=form)

@app.route('/compras')
def compras():
    return render_template('admin/compras.html')

# --- PLACEHOLDERS PARA EVITAR ERRORES FUTUROS ---
# Agrega estas funciones para que cuando el sidebar use url_for no truene el sistema

@app.route('/materia-prima')
def materia_prima():
    return render_template('admin/admin.html')

@app.route('/recetas')
def recetas():
    return render_template('admin/admin.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)