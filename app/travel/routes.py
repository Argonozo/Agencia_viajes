from flask import Blueprint, render_template, redirect, url_for, flash, jsonify,request
from flask_login import login_required, current_user
from app.travel.models import Destination, Package, Reservation
from app.travel.forms import ReservationForm
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


