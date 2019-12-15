from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, PasswordField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput


class ComposeForm(FlaskForm):
    title = StringField('Title')
    tags = StringField('Tags')
    description = TextAreaField('Description', [Length(max=3000)])
    submit = SubmitField('Save')


class ComposePageForm(FlaskForm):
    text = TextAreaField('Content', [Length(max=3000)])
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email')
    password = PasswordField('Password', [DataRequired("Please enter your password.")])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email', [DataRequired("Please enter a email.")])
    password = PasswordField('Password', [DataRequired("Please enter a password.")])
    password2 = PasswordField('Password2', [DataRequired("Please confirm your password.")])
    submit = SubmitField('Sign up')

