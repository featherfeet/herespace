from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, TextAreaField, PasswordField, StringField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()], render_kw = {"placeholder": "Username"})
    password = PasswordField("Password", validators = [DataRequired()], render_kw = {"placeholder": "Password"})
    email = StringField("Email", validators = [DataRequired()], render_kw = {"placeholder": "Email"})
    submit = SubmitField("Submit")
