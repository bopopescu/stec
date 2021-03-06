"""Initializaing the application instance."""
from datetime import datetime, timedelta
import unittest
from flask import current_app
from app import app, db
from app.models import Users, UserPosts


class StecTestCase(unittest.TestCase):
    """Testing the application instance."""

    def setUp(self):
        """Create a database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        """Remove all session."""
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        """Testing the application instance exists."""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Testing the instance is running."""
        self.assertTrue(current_app)


class UsersModelTestCase(unittest.TestCase):
    """Testing the Users Model."""

    def test_password_hash(self):
        """Testing password hash."""
        user = Users(Username='aminat')
        user.set_password('tests')
        self.assertTrue(user.Password is not None)

    def test_password_verify(self):
        """Verifying password hash."""
        user = Users(Username='aminat')
        user.set_password('tests')
        self.assertFalse(user.check_password('testsfalse'))
        self.assertTrue(user.check_password('tests'))

    def test_password_hash_random(self):
        """Testing password hash is random."""
        user1 = Users(Username='aminat')
        user2 = Users(Username='yinka')
        user1.set_password('test')
        user2.set_password('test')
        self.assertTrue(user1.Password != user2.Password)
