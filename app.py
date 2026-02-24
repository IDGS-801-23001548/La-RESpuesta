from flask import Flask, render_template
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'clave-temporal-cambiar-en-produccion'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')


@app.route('/pos')
def pos():
    return render_template('pos/pos.html')

if __name__ == '__main__':
    app.run(debug=True)