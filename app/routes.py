"""Initializaing the application instance."""
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    """Render the index/home page."""
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the Sign in page."""
    # To redirect authenticated/logged in user
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query database to check user credentials
        user = Users.query.filter_by(Username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # Redirect if user credentials is incorrect
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # Redirect if user credentials is correct
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Render the registration page."""
    # To redirect authenticated/logged in user
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(Name=form.name.data, Username=form.username.data, Email=form.email.data, School=form.school.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered member of STEC!!!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    """To logout."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard page."""
    posts = [
        {
            'author': {'Username': 'John'},
            'Body': 'Beautiful day in Portland!'
        },
        {
            'author': {'Username': 'Susan'},
            'Body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('dashboard.html', title='Dashboard', posts=posts)
