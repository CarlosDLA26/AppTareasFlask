from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField(label=None, validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class TodoForm(FlaskForm):
    description = StringField('Descripcion: ', validators=[DataRequired()])
    submit = SubmitField('Crear')