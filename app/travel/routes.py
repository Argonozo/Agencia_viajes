from flask import Blueprint, render_template, redirect, url_for, flash, jsonify,request
from flask_login import login_required, current_user
from app.travel.models import Destination, Package, Reservation
from app.travel.forms import ReservationForm,ReserveDestinationForm,ReservePackageForm
from datetime import datetime
from flask import jsonify
from app import db


travel = Blueprint('travel', __name__)

@travel.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    # Formulario para nuevas reservas
    form = ReservationForm()

    # Cargar dinámicamente los destinos y paquetes disponibles desde la base de datos
    form.destination.choices = [(d.id, d.name) for d in Destination.query.all()]
    form.package.choices = [(p.id, p.name) for p in Package.query.all()]

    if form.validate_on_submit():
        # Crear una nueva reserva asociada al usuario actual
        new_reservation = Reservation(
            user_id=current_user.id,
            destination_id=form.destination.data,
            package_id=form.package.data,
            travel_date=form.travel_date.data
        )
        db.session.add(new_reservation)
        db.session.commit()

        flash('¡Reserva creada correctamente!', 'success')
        return redirect(url_for('travel.reserve'))

    # Obtener las reservas existentes del usuario
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()

    return render_template('travel/reserve.html', form=form, reservations=reservations)

@travel.route('/delete_reservation/<int:id>', methods=['POST'])
@login_required
def delete_reservation(id):
    # Buscar la reserva por ID
    reservation = Reservation.query.get_or_404(id)

    # Verificar que la reserva pertenece al usuario actual
    if reservation.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta reserva.', 'danger')
        return redirect(url_for('travel.reserve'))

    # Eliminar la reserva
    db.session.delete(reservation)
    db.session.commit()
    flash('Reserva eliminada correctamente.', 'success')
    return redirect(url_for('travel.reserve'))

@travel.route('/get_destination_description/<int:destination_id>')
def get_destination_description(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    return jsonify(description=destination.description)



@travel.route('/reserve_package', methods=['GET', 'POST'])
@login_required
def reserve_package():
    form = ReservePackageForm()
    
    # Obtener los paquetes disponibles desde la base de datos
    packages = Package.query.all()
    form.package.choices = [(package.id, package.name) for package in packages]
    
    if form.validate_on_submit():
        # Obtener el ID del paquete seleccionado
        package_id = form.package.data
        travel_date = form.travel_date.data
        
        # Crear y guardar la reserva 
        reservation = Reservation(
            user_id=current_user.id,
            package_id=package_id,
            travel_date=travel_date,
            created_at=datetime.utcnow()
        )
        
        try:
            db.session.add(reservation)
            db.session.commit()
            flash("Reserva realizada con éxito", "success")
            return redirect(url_for('travel.reserve'))
        except Exception as e:
            db.session.rollback()
            flash(f"Hubo un error al realizar la reserva: {str(e)}", "danger")
    
    return render_template('travel/reserve.html', form=form)







from datetime import timedelta

@travel.route('/get_package_dates/<int:package_id>', methods=['GET'])
def get_package_dates(package_id):
    # Obtener el paquete por ID
    package = Package.query.get(package_id)

    if package:
        print(f"Paquete encontrado: {package.name}, Fechas: {package.available_from} - {package.available_to}")
        
        # Crear el rango de fechas en el formato correcto
        date_range = f"{package.available_from.strftime('%Y-%m-%d')} - {package.available_to.strftime('%Y-%m-%d')}"
        print(f"Fechas enviadas al frontend: {date_range}")  # Mostrar la fecha para depuración
        
        return jsonify([date_range])  # Devuelve el rango de fechas como JSON
    else:
        print(f"Paquete no encontrado: {package_id}")
        return jsonify([])  # Si no se encuentra el paquete, devuelve una lista vacía





@travel.route('/get_package_description/<int:package_id>')
def get_package_description(package_id):
    package = Package.query.get_or_404(package_id)
    return jsonify(description=package.description)


@travel.route('/packages')
def packages():
    # Consultar todos los paquetes desde la base de datos
    packages = Package.query.all()
    return render_template('travel/packages.html', packages=packages)

#ruta para reservar destino
@travel.route('/reserve/destination', methods=['GET', 'POST'])
@login_required
def reserve_destination():
    form = ReserveDestinationForm()
    form.destination.choices = [(d.id, d.name) for d in Destination.query.all()]

    if form.validate_on_submit():
        new_reservation = Reservation(
            user_id=current_user.id,
            destination_id=form.destination.data,
            travel_date=form.travel_date.data
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('¡Reserva de destino creada correctamente!', 'success')
        return redirect(url_for('travel.reserve'))

    return render_template('reserve', form=form)

@travel.route('/destinations')
def destinations():
    # Consultar todos los destinos desde la base de datos
    destinations = Destination.query.all()
    return render_template('travel/destinations.html', destinations=destinations)



@travel.route('/home', methods=['GET'])
def home():
    return render_template('travel/home.html')


