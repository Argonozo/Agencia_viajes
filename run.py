from app import create_app, db
from app.auth.models import User  # Esto debería funcionar ahora que los ciclos de importación han sido resueltos

app = create_app()

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
