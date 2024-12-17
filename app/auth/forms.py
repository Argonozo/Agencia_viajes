from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class EditProfileForm(FlaskForm):
    username = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=120)])
    about_me = TextAreaField('Sobre mí', validators=[Length(max=200)])
    password = PasswordField('Nueva contraseña', validators=[Length(min=6, max=50)])
    confirm_password = PasswordField('Confirmar contraseña', 
                                     validators=[EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Actualizar')
    
class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio."),
            Length(min=3, max=80, message="El nombre de usuario debe tener entre 3 y 80 caracteres.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="La contraseña es obligatoria.")
        ]
    )
    submit = SubmitField('Iniciar Sesión')


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio."),
            Length(min=3, max=80, message="El nombre de usuario debe tener entre 3 y 80 caracteres.")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="El correo electrónico es obligatorio."),
            Email(message="Por favor, ingresa un correo electrónico válido.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=8, message="La contraseña debe tener al menos 8 caracteres.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Por favor, confirma tu contraseña."),
            EqualTo('password', message="Las contraseñas deben coincidir.")
        ]
    )
    submit = SubmitField('Registrarse')
