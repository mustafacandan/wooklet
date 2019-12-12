from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, PasswordField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput

class compose_form(FlaskForm):
    title = StringField('Title')
    tags = StringField('Tags')
    description = TextAreaField('Description', [Length(max=3000)])
    submit = SubmitField('Save')

class compose_page_form(FlaskForm):
    text = TextAreaField('Content', [Length(max=3000)])
    submit = SubmitField('Save')

class login_form(FlaskForm):
    username_or_email = StringField('Username or Email')
    password = PasswordField('Password', [DataRequired("Please enter your password.")])
    submit = SubmitField('Login')

class signup_form(FlaskForm):
    username = StringField('Username')
    email = StringField('Email', [DataRequired("Please enter a email.")])
    # password = StringField('Password', widget=PasswordInput(hide_value=False))
    password = PasswordField('Password', [DataRequired("Please enter a password.")])
    submit = SubmitField('Sign up')

