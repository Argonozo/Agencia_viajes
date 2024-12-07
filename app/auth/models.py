from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db



class User(UserMixin, db.Model): # herencia de usermixin para permitir gesiton de sesiones
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='client')  # Puede ser 'client' o 'admin'
    reservations = db.relationship('Reservation', backref='owner', lazy=True)

    def set_password(self, password):
        """Genera un hash para la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña proporcionada con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
