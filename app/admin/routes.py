from flask import Blueprint, render_template,redirect,url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.auth.models import User
from app.travel.models import Reservation, Destination,Package
from app.travel.forms import PackageForm
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


###
###      CRUD       ###
###     Usuarios    ###
###
# Ruta para listar todos los usuarios
@admin.route('/users')
@login_required
def users():
    users = User.query.all()  # Obtener todos los usuarios
    return render_template('admin/users.html', users=users)

#
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



###
###      CRUD       ###
###     Paquetes   ###
###

# Ruta para listar todos los paquetes
@admin.route('/packages')
@login_required
def manage_packages():
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('auth.login'))

    packages = Package.query.all()

    if not packages:
        flash('No se encontraron paquetes turísticos.', 'warning')

    return render_template('admin/packages.html', packages=packages)

# Ruta para agregar un nuevo paquete
@admin.route('/packages/add', methods=['GET', 'POST'])
@login_required
def add_package():
    form = PackageForm()
    form.destinations.choices = [(d.id, d.name) for d in Destination.query.all()]
    
    if form.validate_on_submit():
        # Asegurarse de que los campos de fecha estén siendo asignados
        package = Package(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            available_from=form.available_from.data,  # Asignar campo available_from
            available_to=form.available_to.data       # Asignar campo available_to
        )
        
        # Asociar destinos seleccionados
        package.destinations = Destination.query.filter(Destination.id.in_(form.destinations.data)).all()
        
        db.session.add(package)
        db.session.commit()
        return redirect(url_for('admin.manage_packages'))
    
    return render_template('admin/add_package.html', form=form)


# Ruta para editar un paquete
@admin.route('/packages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_package(id):
    package = Package.query.get_or_404(id)
    form = PackageForm(obj=package)

    # Configurar opciones de destinos para el formulario
    form.destinations.choices = [(d.id, d.name) for d in Destination.query.all()]

    if form.validate_on_submit():
        package.name = form.name.data
        package.description = form.description.data
        package.price = form.price.data
        package.available_from = form.available_from.data  # Usar available_from
        package.available_to = form.available_to.data  # Usar available_to

        # Actualizar destinos asociados
        package.destinations = Destination.query.filter(Destination.id.in_(form.destinations.data)).all()

        db.session.commit()
        flash('Paquete turístico actualizado exitosamente.', 'success')
        return redirect(url_for('admin.manage_packages'))

    # Preseleccionar destinos asociados al paquete
    form.destinations.data = [d.id for d in package.destinations]

    return render_template('admin/edit_package.html', form=form, package=package)


# Ruta para eliminar un paquete
@admin.route('/packages/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_package(id):
    if request.method == 'POST':
        package = Package.query.get_or_404(id)
        db.session.delete(package)
        db.session.commit()
        flash('Paquete turístico eliminado exitosamente.', 'success')
    return redirect(url_for('admin.manage_packages'))
