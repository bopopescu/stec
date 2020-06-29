"""Initializaing the application instance."""
from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    """Render the index/home page."""
    return render_template('index.html', title='Home')
