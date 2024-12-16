from app import create_app, db
from app.auth.models import User  # Ajusta el import si tu modelo está en otro módulo

# Inicializa la aplicación y el contexto
app = create_app()
app.app_context().push()

# Verifica si ya existe un administrador
existing_admin = User.query.filter_by(username='admin').first()
if not existing_admin:
    # Crea un usuario administrador genérico
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    admin.set_password('admin123')  # Establece una contraseña para el administrador

    # Agrega el usuario a la base de datos
    db.session.add(admin)
    db.session.commit()

    print("Usuario administrador creado con éxito.")
else:
    print("El usuario administrador ya existe.")
