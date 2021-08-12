from flask import request, make_response, redirect, url_for, render_template, session
from app.firestore_service import get_todos, get_users, register_todo, delete_todo, set_state
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap
from app.forms import *
from app import create_app
from flask import flash
import unittest

app = create_app()

@app.cli.command()
def test():
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(test)

@app.route('/')
def index():
    # Guardamos la ip del usuario en una variable
    # user_ip = request.remote_addr
    # creamos una respuesta redireccionandola a la ruta /hello
    response = make_response(redirect('/hello'))
    # En la respuesta guardamo una cookie con clave user_ip y valor user_ip
    # session['user_ip'] = user_ip
    return response

# Se define una ruta donde se ejecuta el metodo hello_world
@app.route("/hello", methods=['GET', 'POST'])
@login_required
def hello_world():
    username = current_user.id
    todo_form = TodoForm()

    # for user in users:
    #     print(f'{user.id} -> {user.to_dict()}')

    context = {
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
    }

    if todo_form.validate_on_submit():
        register_todo(username, todo_form.description.data)
        flash('Tarea creada con exito')

        return redirect(url_for('hello_world'))

    return render_template('hello.html', **context)

# <todo_id> es una ruta dinamica que se puede usar en flask
@app.route('/todos/delete/<todo_id>', methods=['GET', 'POST'])
def delete(todo_id):
    delete_todo(current_user.id, todo_id)
    return redirect(url_for('hello_world'))

@app.route('/todos/set_activity/<todo_id>/<int:done>', methods=['GET', 'POST'])
def set_activity(todo_id, done):
    set_state(current_user.id, todo_id, done)
    return redirect(url_for('hello_world'))

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', error=error)