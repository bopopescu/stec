"""Initializaing the application instance."""
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Users, Posts


class UserModelCase(unittest.TestCase):
    """Testing different functions."""

    def setUp(self):
        """Create a database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        """Remove all session."""
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        """Testing password hash."""
        u = Users(Username='aminat')
        u.set_password('tests')
        self.assertFalse(u.check_password('testsfalse'))
        self.assertTrue(u.check_password('tests'))

    # def test_avatar(self):
    #     """Testing avatar generation."""
    #     u = Users(Name='Abolore Mina', Username='Abololz',
    #               Email='mina@tests.com')
    #     self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
    #                                      '205e460b479e2e5b48aec07710c08d50'
    #                                      '?d=identicon&s=128'))

    def test_posts(self):
        """Testing post."""
        # create four users
        u1 = Users(Name='john doe', Username='john', Email='john@example.com')
        u2 = Users(Name='susan wilson', Username='susan',
                   Email='susan@example.com')
        u3 = Users(Name='mary jane', Username='mary', Email='mary@example.com')
        u4 = Users(Name='david williams', Username='david',
                   Email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Posts(Subject='testing 1', Body="post from john", author=u1,
                   Timestamp=now + timedelta(seconds=1))
        p2 = Posts(Subject='testing 2', Body="post from susan", author=u2,
                   Timestamp=now + timedelta(seconds=4))
        p3 = Posts(Subject='testing 3', Body="post from mary", author=u3,
                   Timestamp=now + timedelta(seconds=3))
        p4 = Posts(Subject='testing 4', Body="post from david", author=u4,
                   Timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
