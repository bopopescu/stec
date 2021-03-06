"""Initializaing the application instance."""
from flask import render_template
from app import app, db


@app.errorhandler(404)
def page_not_found_error(error):
    """Render the page for error 404."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Render the page for error 500."""
    db.session.rollback()
    return render_template('500.html'), 500
