"""Initializaing the application instance."""
from datetime import datetime
from app import db


class Users(db.Model):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150), index=True)
    Username = db.Column(db.String(15), index=True, unique=True)
    Email = db.Column(db.String(120), index=True, unique=True)
    School = db.Column(db.String(250), index=True)
    Password = db.Column(db.String(128))
    Posts = db.relationship('Posts', backref='author', lazy='dynamic')

    def __repr__(self):
        """For testing."""
        return '<Your username is: {}>'.format(self.Username)


class Posts(db.Model):
    __tablename__ = 'Posts'

    PostID = db.Column(db.Integer, primary_key=True)
    Subject = db.Column(db.String(50))
    Body = db.Column(db.String(250))
    Timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))

    def __repr__(self):
        """For testing."""
        return '<Post subject: {} and body: {}>'.format(self.Subject, self.Body)
