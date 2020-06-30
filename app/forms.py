"""Initializaing the application instance."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Users

class LoginForm(FlaskForm):
    """Login Form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    """Registration Form."""

    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    school = StringField('School', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, Username):
        user = Users.query.filter_by(Username=Username.data).first()
        if user is not None:
            raise ValidationError('Username not available.')

    def validate_email(self, Email):
        user = Users.query.filter_by(Email=Email.data).first()
        if user is not None:
            raise ValidationError('Account with this email address exists.')
