from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, TextAreaField, PasswordField, StringField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    submit = SubmitField("Submit")
