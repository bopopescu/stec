"""Initializaing the application instance."""
import os
import sys
import click
from app import app, db
from app.models import Users, Posts, UserPosts, Contacts, \
        UserMessages, Notifications


@app.shell_context_processor
def make_shell_context():
    """Database tables."""
    return dict(db=db, Users=Users, Posts=Posts, UserPosts=UserPosts,
                Contacts=Contacts, UserMessages=UserMessages,
                Notifications=Notifications)


COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()



if __name__ == '__main__':
    app.run()
