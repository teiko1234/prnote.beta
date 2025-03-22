from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)

# Modèle utilisateur avec rôles
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'eleve', 'prof', 'vie_scolaire', 'direction'

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return 'Identifiants incorrects', 401
    return render_template('login.html')

# Tableau de bord redirigé selon le rôle
@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))
    role = session['role']
    if role == 'eleve':
        return render_template('dashboard_eleve.html')
    elif role == 'prof':
        return render_template('dashboard_prof.html')
    elif role == 'vie_scolaire':
        return render_template('dashboard_vie_scolaire.html')
    elif role == 'direction':
        return render_template('dashboard_direction.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
