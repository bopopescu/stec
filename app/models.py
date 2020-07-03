"""Initializaing the application instance."""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from hashlib import md5


class Users(UserMixin, db.Model):
    """Users table query."""

    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150), index=True, nullable=False)
    Username = db.Column(db.String(15), index=True, unique=True, nullable=False)
    Email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    Bio = db.Column(db.String(150))
    DateOfBirthday = db.Column(db.DateTime)
    Gender = db.Column(db.String(30))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    Password = db.Column(db.String(128))
    Posts = db.relationship('Posts', backref='author', lazy='dynamic')

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


class Posts(db.Model):
    """Posts table query."""

    __tablename__ = 'Posts'

    PostID = db.Column(db.Integer, primary_key=True)
    Subject = db.Column(db.String(50), nullable=False)
    Body = db.Column(db.String(250), nullable=False)
    Timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))

    def __repr__(self):
        """For testing."""
        return '<Post subject: {} and body: {}>'.format(self.Subject, self.Body)
