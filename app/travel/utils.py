from app.travel.models import Destination, Package, Booking
from app import db

def get_available_packages(start_date, end_date):
    """
    Obtiene los paquetes disponibles para las fechas especificadas.
    """
    return Package.query.filter(Package.start_date >= start_date, Package.end_date <= end_date, Package.is_available).all()

def create_booking(user, package, start_date, end_date):
    """
    Crea una nueva reserva para el usuario y el paquete especificados.
    """
    booking = Booking(user=user, package=package, start_date=start_date, end_date=end_date)
    db.session.add(booking)
    db.session.commit()
    return booking