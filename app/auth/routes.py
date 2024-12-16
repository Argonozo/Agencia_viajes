from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import LoginForm, RegisterForm, EditProfileForm
from app.auth.models import  User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("validacion correcta")
        user = User.query.filter_by(email=form.email.data).first()  # Buscar por email
        if user and user.check_password(form.password.data):
            ## print(f"Usuario autenticado")
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            #redirige segun el rol
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('auth.profile'))  # Redirigir a la vista correcta
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('El nombre de usuario o correo electrónico ya está registrado.', 'danger')
        else:
            new_user = User(
                username=form.username.data,
                email=form.email.data
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Cuenta creada exitosamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))  # Redirige al login sin iniciar sesión
    return render_template('auth/register.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión con éxito.', 'success')
    return redirect(url_for('auth.login'))  # Redirige a la página de login

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(obj=current_user)  # Prellenar con datos del usuario actual

    if form.validate_on_submit():
        # Actualizar datos del usuario actual
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', form=form)


