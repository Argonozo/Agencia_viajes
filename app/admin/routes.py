from flask import Blueprint, render_template,redirect,url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.auth.models import User
from app.travel.models import Reservation, Destination,Package
from app.admin.forms import DestinationForm
from app import db


admin = Blueprint('admin', __name__, template_folder='templates' )

def admin_requiered(func):
    @login_required
    def wrapper (*args, **kwargs):
        if not current_user.is_admin(): #usa el metodo is_admin del modelo de usuario
            flash('acceso denegado:solo administradores pueden acceder')
            return redirect(url_for('auth.login'))
        return func (*args, **kwargs)
    wrapper.__name__ = func.__name__ # flask requiere el nombre del wrap
    return wrapper



# Ruta para el panel de administración (dashboard)
@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':  # Verificar rol del usuario
        flash('Acceso denegado: solo administradores pueden acceder.', 'danger')
        return redirect(url_for('auth.login'))

    # Contadores
    user_count = User.query.count()
    destination_count = Destination.query.count()
    package_count = Package.query.count()

    return render_template(
        'admin/dashboard.html',
        user_count=user_count,
        destination_count=destination_count,
        package_count=package_count
    )


# Ruta para listar todos los usuarios
@admin.route('/users')
@login_required
def users():
    users = User.query.all()  # Obtener todos los usuarios
    return render_template('admin/users.html', users=users)

###
###      CRUD       ###
###     Usuarios    ###
###
# Ruta para crear un nuevo usuario
@admin.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        # Alos datos del formulario
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # Asegúrate de encriptar la contraseña

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuario creado exitosamente!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/create_user.html')  # Formulario para crear usuario

# Ruta para editar un usuario
@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role =request.form['role']
        
        if request.form['password']:
            user.password =request.form['password']
        db.session.commit()

        flash('Usuario actualizado exitosamente!', 'success')
        return redirect(url_for('admin.users'))
    #obtener las reservas asociadas al usuario
    reservations = Reservation.query.filter_by(user_id=id).all()

    return render_template('admin/edit_user.html', user=user, reservations = reservations)  # Formulario para editar usuario

# Ruta para eliminar un usuario
@admin.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    flash('Usuario eliminado exitosamente!', 'success')
    return redirect(url_for('admin.users'))

###
###      CRUD       ###
###     Destinos    ###
###


# Ruta para listar todos los destinos
@admin.route('/destinations')
@login_required
def manage_destinations():
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('auth.login'))
    
    
    destinations = Destination.query.all()

    # Verifica si se recuperaron destinos
    if not destinations:
        flash('No se encontraron destinos.', 'warning')

    return render_template('admin/destinations.html', destinations=destinations)


# Ruta para agregar un nuevo destino


@admin.route('/destinations/add', methods=['GET', 'POST'])
@login_required
def add_destination():
    form = DestinationForm()

    if request.method == 'POST':  # Solo procesa si la solicitud es POST
        if form.validate_on_submit():
            # Crear un nuevo destino
            destination = Destination(
                name=form.name.data,
                description=form.description.data,
                activities=form.activities.data,
                cost=form.cost.data
            )
            # Agregarlo a la base de datos
            db.session.add(destination)
            db.session.commit()

            flash('Destino agregado exitosamente', 'success')
            return redirect(url_for('admin.manage_destinations'))  # Redirige a la lista de destinos
        else:
            # Imprimir errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error en {field}: {error}")
            flash("No se guardó nada", "error")

    return render_template('admin/add_destination.html', form=form)




# Ruta para editar un destino
@admin.route('/destinations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_destination(id):
    destination = Destination.query.get_or_404(id)
    form = DestinationForm(obj=destination)

    if form.validate_on_submit():
        destination.name = form.name.data
        destination.description = form.description.data
        destination.activities = form.activities.data
        destination.cost = form.cost.data
        
        db.session.commit()
        flash('Destino actualizado exitosamente.', 'success')
        return redirect(url_for('admin.manage_destinations'))

    return render_template('admin/edit_destination.html', form=form, destination=destination)


# Ruta para eliminar un destino
@admin.route('/destinations/delete/<int:id>', methods=['POST'])
@login_required
def delete_destination(id):
    destination = Destination.query.get_or_404(id)
    db.session.delete(destination)
    db.session.commit()
    flash('Destino eliminado exitosamente.', 'success')
    return redirect(url_for('admin.manage_destinations'))


@admin.route('/reservations/delete/<int:id>', methods=['POST'])
@login_required
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    
    # Verificar si el usuario actual tiene permisos para eliminar
    if current_user.role != 'admin':
        flash('No tienes permiso para eliminar esta reserva.', 'danger')
        return redirect(request.referrer or url_for('admin.users'))

    # Proceder a eliminar la reserva si el usuario es administrador
    db.session.delete(reservation)
    db.session.commit()
    flash('Reserva eliminada exitosamente.', 'success')
    return redirect(request.referrer or url_for('admin.users'))



#crud paquetes_Adin
@admin.route('/manage-packages', methods=['GET'])
def manage_packages():
    # Aquí puedes agregar la lógica para listar o gestionar paquetes
    return render_template('admin/manage_packages.html')