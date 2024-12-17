from flask import Blueprint, render_template, redirect, url_for, flash, jsonify,request
from flask_login import login_required, current_user
from app.travel.models import Destination, Package, Reservation
from app.travel.forms import ReservationForm
from datetime import timedelta
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



@travel.route('/reserve_package', methods=['POST'])
@login_required
def reserve_package():
    package_id = request.form.get('package')
    travel_date = request.form.get('travel_date_pack')
    if package_id and travel_date:
        new_reservation = Reservation(
            user_id=current_user.id,
            package_id=package_id,
            travel_date=travel_date
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('¡Reserva de paquete creada correctamente!', 'success')
    else:
        flash('Por favor selecciona un paquete y una fecha válida.', 'danger')
    return redirect(url_for('travel.reserve'))




@travel.route('/get_package_dates/<int:package_id>', methods=['GET'])
def get_package_dates(package_id):
    package = Package.query.get(package_id)
    if package:
        start_date = package.available_from
        end_date = package.available_to
        delta = (end_date - start_date).days
        dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta + 1)]
        return {'dates': dates}, 200
    return {'dates': []}, 404




@travel.route('/get_package_description/<int:package_id>')
def get_package_description(package_id):
    package = Package.query.get_or_404(package_id)
    return jsonify(description=package.description)


@travel.route('/packages')
def packages():
    # Consultar todos los paquetes desde la base de datos
    packages = Package.query.all()
    return render_template('travel/packages.html', packages=packages)


@travel.route('/destinations')
def destinations():
    # Consultar todos los destinos desde la base de datos
    destinations = Destination.query.all()
    return render_template('travel/destinations.html', destinations=destinations)



@travel.route('/home', methods=['GET'])
def home():
    return render_template('travel/home.html')


