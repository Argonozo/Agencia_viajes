from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired

class DestinationForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    activities = StringField('Actividades', validators=[DataRequired()])
    cost = FloatField('Costo', validators=[DataRequired()])
