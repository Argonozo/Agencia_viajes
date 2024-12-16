from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField,StringField,FloatField,SelectMultipleField
from wtforms.validators import DataRequired
# Formulario para crear una reserva
class ReservationForm(FlaskForm):
    destination = SelectField('Destino', coerce=int, validators=[DataRequired()])
    package = SelectField('Paquete Turístico', coerce=int, validators=[DataRequired()])
    travel_date = DateField('Fecha de Viaje', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Reservar')

class PackageForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    price = FloatField('Precio', validators=[DataRequired()])
    destinations = SelectMultipleField('Destinos', coerce=int)  # IDs de destinos
    available_from = DateField('Disponible Desde', format='%Y-%m-%d')
    available_to = DateField('Disponible Hasta', format='%Y-%m-%d')
    submit = SubmitField('Guardar')