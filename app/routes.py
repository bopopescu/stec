"""Initializaing the application instance."""
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    """Render the index/home page."""
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the Sign in page."""
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login successful for user {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)
