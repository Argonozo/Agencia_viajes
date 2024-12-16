

class Config:
    SECRET_KEY = 'mi_clave_secreta'  # Cambia esto por una clave segura
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Usando SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
