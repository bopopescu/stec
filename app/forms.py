"""Initializaing the application instance."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
        DateField, RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, \
        Email, EqualTo, Length
from app.models import Users


class LoginForm(FlaskForm):
    """Login Form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    """Registration Form."""

    name = StringField('Name', validators=[
                       DataRequired(), Length(min=5, max=150)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dateofbirth = DateField(
        'Date Of Birth', format='%m/%d/%Y', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[
        ('F', 'Female'), ('M', 'Male'), ('O', 'Prefer not to choose')],
                validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                              DataRequired(), Length(min=7, max=15)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), Length(min=7, max=15),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, Username):
        user = Users.query.filter_by(Username=Username.data).first()
        if user is not None:
            raise ValidationError('Username not available.')

    def validate_email(self, Email):
        user = Users.query.filter_by(Email=Email.data).first()
        if user is not None:
            raise ValidationError('Account with this email address exists.')


class EditProfileForm(FlaskForm):
    """Edit Profile Form."""

    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=150)])
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, Username):
        if Username.data != self.original_username:
            user = Users.query.filter_by(Username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username not available.')


class UserPostForm(FlaskForm):
    """User Post Form."""

    body = TextAreaField('Post', validators=[
        DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Submit')
