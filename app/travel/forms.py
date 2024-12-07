from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

# Formulario para crear una reserva
class ReservationForm(FlaskForm):
    destination = SelectField('Destino', coerce=int, validators=[DataRequired()])
    package = SelectField('Paquete Turístico', coerce=int, validators=[DataRequired()])
    travel_date = DateField('Fecha de Viaje', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Reservar')
