"""Initializaing the application instance."""
from datetime import datetime, timedelta
import unittest
from flask import current_app
from app import app, db


class StecTestCase(unittest.TestCase):
    """Testing different functions."""

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
