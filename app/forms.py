"""Initializaing the application instance."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
        SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, \
        Email, EqualTo, Length, Regexp
from app.models import Users


class ContactForm(FlaskForm):
    """Contact Form in index page."""

    name = StringField('Name', validators=[
                DataRequired(), Length(min=5, max=150),])
    email = StringField('Email', validators=[DataRequired(), Email()])
    enquiry = TextAreaField('Enquiry', validators=[
        DataRequired(), Length(min=5)])
    submit = SubmitField('Submit')

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
                DataRequired(), Length(min=5, max=15),
                Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Username must have only letters, numbers, dots or '
               'underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                DataRequired(), Length(min=7, max=15)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), Length(min=7, max=15),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, Username):
        """Verify that the Username is unique."""
        user = Users.query.filter_by(Username=Username.data).first()
        if user is not None:
            raise ValidationError('Username not available.')

    def validate_email(self, Email):
        """Verify that the Email is unique."""
        user = Users.query.filter_by(Email=Email.data).first()
        if user is not None:
            raise ValidationError('Account with this email already exists.')


class EditProfileForm(FlaskForm):
    """Edit Profile Form."""

    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=150)])
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        """Verify that the initial Username."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, Username):
        """Verify that the Username is unique and not the same."""
        if Username.data != self.original_username:
            user = Users.query.filter_by(Username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username not available.')


class UserPostForm(FlaskForm):
    """User Post Form."""

    body = TextAreaField('Post', validators=[DataRequired(),
                                             Length(min=1, max=150)])
    submit = SubmitField('Submit')


class UserPostEditForm(FlaskForm):
    """User Post Edit Form."""

    body = TextAreaField('Post', validators=[DataRequired(),
                                             Length(min=1, max=150)])
    submit = SubmitField('Update')


class UserPostDeleteForm(FlaskForm):
    """User Post Delete Form."""

    body = TextAreaField('Post', validators=[DataRequired(),
                                             Length(min=1, max=150)])
    submit = SubmitField('Delete')


class PasswordResetRequestForm(FlaskForm):
    """Password Reset Request Form."""

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    """Password Reset Form."""

    password = PasswordField('Password', validators=[
                DataRequired(), Length(min=7, max=15)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), Length(min=7, max=15),
                                       EqualTo('password')])
    submit = SubmitField('Password Reset')


class UserMessageForm(FlaskForm):
    """User Message Form."""

    message = TextAreaField('Private Message', validators=[DataRequired(),
                                                           Length(min=10,
                                                                  max=200)])
    submit = SubmitField('Submit Message')


# Adminstrator forms starts here
class AdminPostForm(FlaskForm):
    """Admin Post Form."""

    subject = StringField('Title', validators=[DataRequired(), Length(min=10)])
    body = TextAreaField('Article', validators=[DataRequired(),
                                                Length(min=100)])
    submit = SubmitField('Submit')


class AdminPostEditForm(FlaskForm):
    """Admin Post Edit Form."""

    subject = StringField('Title', validators=[DataRequired(), Length(min=10)])
    body = TextAreaField('Article', validators=[DataRequired(),
                                                Length(min=100)])
    submit = SubmitField('Update')


class AdminPostDeleteForm(FlaskForm):
    """Admin Post Delete Form."""

    subject = StringField('Title', validators=[DataRequired(), Length(min=10)])
    body = TextAreaField('Article', validators=[DataRequired(),
                                                Length(min=100)])
    submit = SubmitField('Delete')
