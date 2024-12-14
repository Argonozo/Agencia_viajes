from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from os import path

# Inicializar la base de datos fuera de la función `create_app`
db = SQLAlchemy()
login_manager = LoginManager()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Cargar la configuración de la app desde config.py
    db.init_app(app)  # Inicializar la base de datos
    login_manager.init_app(app)  # Inicializar Flask-Login
    
    # Definir el user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.auth.models import User  # Importación aquí para evitar el ciclo
        return User.query.get(int(user_id))  # Buscar al usuario por su ID

    # Registrar Blueprints
    from app.auth.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')  # Usar '/auth' como prefijo
    
    from app.travel.routes import travel
    app.register_blueprint(travel, url_prefix='/reserve')

    from app.admin.routes import admin
    app.register_blueprint(admin, url_prefix = '/admin')    
    
    # Ruta principal
    @app.route('/')
    def index():
        return redirect(url_for('travel.home'))  # Redirigir al login si no está autenticado
    

    return app

def create_database(app):
    """Función para crear la base de datos si no existe"""
    if not path.exists('instance/' + DB_NAME):  # Usar 'instance' para mayor organización
        with app.app_context():
            db.create_all()  # Crear las tablas de la base de datos
            print('Created Database!')
