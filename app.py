from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.secret_key = '092717!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:huevos123@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

class User(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(nombre_usuario=username, contraseña=password).first()

        if user:
            return redirect(url_for('home', nombre=user.nombre_completo))
        else:
            flash('Credenciales incorrectas. Intenta de nuevo.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(nombre_usuario=username).first()

        if existing_user:
            return jsonify({'status': 'error', 'message': 'Ya existe un usuario con este correo electrónico. Por favor, elige otro.'})
        else:
            new_user = User(nombre_completo=nombre_completo, nombre_usuario=username, contraseña=password)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('home', nombre=nombre_completo))

    return render_template('register.html')


@app.route('/home/<nombre>')
def home(nombre):
    return render_template('home.html', nombre=nombre)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
    