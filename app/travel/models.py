from app import db
from datetime import datetime

class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    activities = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    # Relación con reservas, renombrando el backref para evitar conflicto
    reservations = db.relationship('Reservation', backref='destination_related', lazy=True)

    def __repr__(self):
        return f'<Destination {self.name}>'


# Tabla intermedia
package_destinations = db.Table('package_destinations',
    db.Column('package_id', db.Integer, db.ForeignKey('packages.id'), primary_key=True),
    db.Column('destination_id', db.Integer, db.ForeignKey('destinations.id'), primary_key=True)
)

class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_from = db.Column(db.Date, nullable=False)
    available_to = db.Column(db.Date, nullable=False)

    # Relación con Reservation
    reservations = db.relationship('Reservation', backref='package_related', lazy=True)

    # Relación con Destination
    destinations = db.relationship('Destination', secondary=package_destinations, backref=db.backref('packages', lazy='dynamic'))

    def __repr__(self):
        return f'<Package {self.name}>'


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=True)  # Relación con Destination
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=True)  # Relación con Package
    travel_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con Destination (opcional, ya que destination_id es nullable)
    destination = db.relationship('Destination', backref='reservations_related', lazy=True)
    
    # Relación con Package (opcional, ya que package_id es nullable)
    package = db.relationship('Package', backref='reservations_related', lazy=True)

    # Relación con User 
    user = db.relationship('User', backref='user_reservations', lazy=True)

    def __repr__(self):
        return f'<Reservation {self.id}>'
