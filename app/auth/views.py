from flask_login import login_user, login_required, logout_user
from flask import flash, redirect, url_for, session
from app.firestore_service import get_user, register_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import UserData, UserModel
from flask import render_template
from app.forms import LoginForm
from . import auth

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            register_user(username, password_hash)
            # Se loguea el usuario que se acaba de crear
            login_user(UserModel(UserData(username, password_hash)))

            flash('Bienvenido de nuevo')

            return redirect(url_for('hello_world'))

        
        else:
            flash(f'El usuario "{username}" ya existe')
        
    context = {
        'signup_form': signup_form
    }

    return render_template('signup.html', **context)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    # Procesar formulario
    # validate_on_submit
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            # Verificar a traves de password hasheada
            if check_password_hash(password_from_db, password):
                # Usar el archivo models para hacer el login
                user = UserModel(UserData(username, password))

                login_user(user)
                flash('Bienvenido de nuevo', category='message')
                redirect(url_for('hello_world'))
            else:
                flash('La contraseña es incorrecta', category='message')

        else: 
            flash('No se ha encontrado el usuario')

        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa Pronto')
    return redirect(url_for('auth.login'))