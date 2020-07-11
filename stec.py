"""Initializaing the application instance."""
from app import app, db
from app.models import Users, Posts, UserPosts, Contacts, \
        UserMessages, Notifications


@app.shell_context_processor
def make_shell_context():
    """Database tables."""
    return dict(db=db, Users=Users, Posts=Posts, UserPosts=UserPosts,
                Contacts=Contacts, UserMessages=UserMessages,
                Notifications=Notifications)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run()
