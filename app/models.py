"""Initializaing the application instance."""
from datetime import datetime
from hashlib import md5
from time import time
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login, app
import jwt


class Users(UserMixin, db.Model):
    """Users table query."""

    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150), index=True, nullable=False)
    Username = db.Column(db.String(15), index=True,
                         unique=True, nullable=False)
    Email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    Bio = db.Column(db.String(150))
    Password = db.Column(db.String(128), nullable=False)
    LastSeen = db.Column(db.DateTime, default=datetime.utcnow)
    LastMessageReadTime = db.Column(db.DateTime)
    RegisteredDate = db.Column(db.DateTime, nullable=False,
                               default=datetime.utcnow)
    StecAdmin = db.Column(db.Boolean, nullable=False, default=False)
    Confirmed = db.Column(db.Boolean, nullable=False, default=False)
    ConfirmedDate = db.Column(db.DateTime)
    UserPosts = db.relationship('UserPosts', backref='author', lazy='dynamic')
    StecPosts = db.relationship('Posts', backref='author', lazy='dynamic')
    MessageSent = db.relationship('UserMessages',
                                  foreign_keys='UserMessages.SenderID',
                                  backref='author', lazy='dynamic')
    MessageReceived = db.relationship('UserMessages',
                                      foreign_keys='UserMessages.ReceiverID',
                                      backref='receiver', lazy='dynamic')
    Notification = db.relationship('Notifications', backref='user',
                                   lazy='dynamic')

    def set_password(self, Password):
        """To hash user's password."""
        self.Password = generate_password_hash(Password)

    def check_password(self, Password):
        """To verify user's password hash."""
        return check_password_hash(self.Password, Password)

    def __repr__(self):
        """For testing."""
        return '<Your username is: {}>'.format(self.Username)

    def get_id(self):
        """Return the user id for Flask-Login's requirements."""
        return self.UserID

    @login.user_loader
    def load_user(UserID):
        """Query to retrieve user ID."""
        return Users.query.get(int(UserID))

    def avatar(self, size):
        """Using email to generate an avatar."""
        digest = md5(self.Email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=1800):
        """Generating password reset token."""
        return jwt.encode(
            {'password_reset': self.UserID, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """verify password reset token."""
        try:
            UserID = jwt.decode(token, app.config['SECRET_KEY'],
                                algorithms=['HS256'])['password_reset']
        except:
            return False
        return Users.query.get(int(UserID))

    def new_messages(self):
        last_read_time = self.LastMessageReadTime or datetime(2000, 1, 1)
        return UserMessages.query.filter_by(receiver=self).filter(
            UserMessages.Timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.Notification.filter_by(Name=name).delete()
        new = Notifications(Name=name, Payload_json=json.dumps(data),
                            user=self)
        db.session.add(new)
        return new


class UserPosts(db.Model):
    """User Posts table query."""

    __tablename__ = 'UserPosts'

    UserPostID = db.Column(db.Integer, primary_key=True)
    Body = db.Column(db.String(250), nullable=False)
    Timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))

    def __repr__(self):
        """For testing."""
        return '<User Post body: {}>'.format(self.Body)


class Contacts(db.Model):
    """Contact table query."""

    __tablename__ = 'Contacts'

    ContactID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150), index=True, nullable=False)
    Email = db.Column(db.String(120), index=True, nullable=False)
    Enquiry = db.Column(db.Text(), nullable=False)
    Timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """For testing."""
        return '<{}: your enquiry is submitted>'.format(self.Name)


class UserMessages(db.Model):
    """User message table query."""

    __tablename__ = 'UserMessages'

    UserMessageID = db.Column(db.Integer, primary_key=True)
    SenderID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    ReceiverID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    Body = db.Column(db.String(200))
    Timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """For testing."""
        return '<User Message is: {}>'.format(self.Body)


class Notifications(db.Model):
    """Notification table query."""

    __tablename__ = 'Notifications'

    N_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150), index=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    Timestamp = db.Column(db.Float, index=True, default=time)
    Payload_json = db.Column(db.Text)

    def get_data(self):
        """Show Notifications."""
        return json.loads(str(self.Payload_json))


# Adminstrator models starts here
class Posts(db.Model):
    """Posts table query."""

    __tablename__ = 'Posts'

    PostID = db.Column(db.Integer, primary_key=True)
    Subject = db.Column(db.String(100), nullable=False)
    Body = db.Column(db.Text(), nullable=False)
    Timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    StecAdminID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))

    def __repr__(self):
        """For testing."""
        return '<Post subject: {} and body: {}>'.format(self.Subject,
                                                        self.Body)
