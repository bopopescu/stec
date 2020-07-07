"""Initializaing the application instance."""
from app import app, db
from app.models import Users, Posts, UserPosts, Contacts


@app.shell_context_processor
def make_shell_context():
    """Database tables."""
    return {'db': db, 'Users': Users, 'Posts': Posts, 'UserPosts': UserPosts,
            'Contacts': Contacts}


if __name__ == '__main__':
    app.run()
