"""Initializaing the application instance."""
from app import app, db
from app.models import Users, Posts


@app.shell_context_processor
def make_shell_context():
    """Database tables."""
    return {'db': db, 'Users': Users, 'Posts': Posts}


# if __name__ == '__main__':
#     app.run(debug=True)
