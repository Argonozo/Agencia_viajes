from app import create_app, db
from app.travel.models import Destination

# Crear la app
app = create_app()

# Establecer el contexto de la aplicación
with app.app_context():
    destinos = Destination.query.all()
    for destino in destinos:
        print(destino.name)
