"""Initializaing the application instance."""
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, UserPostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, UserPosts
from werkzeug.urls import url_parse
from datetime import datetime


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
        user = Users(Name=form.name.data, Username=form.username.data,
                     Email=form.email.data,
                     DateOfBirthday=form.dateofbirth.data,
                     Gender=form.gender.data)
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


@app.route('/dashboard', methods=['GET', 'POST'])
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


@app.route('/profile/<Username>', methods=['GET', 'POST'])
@login_required
def profile(Username):
    """Render the user profile page."""
    user = Users.query.filter_by(Username=Username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = UserPosts.query.order_by(UserPosts.Timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('members_post', Username=user.Username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('members_post', Username=user.Username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('profile.html', title='Profile', user=user, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Render the page for profile editing."""
    form = EditProfileForm(current_user.Username)
    if form.validate_on_submit():
        current_user.Username = form.username.data
        current_user.Bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.Username
        form.bio.data = current_user.Bio
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.before_request
def before_request():
    """Render the date user login previously."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@app.route('/members_post', methods=['GET', 'POST'])
@login_required
def members_post():
    """Render the member post page."""
    form = UserPostForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        post = UserPosts(Body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post upload successful')
        return redirect(url_for('members_post'))
    posts = UserPosts.query.order_by(UserPosts.Timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('members_post', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('members_post', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('members_post.html', title='Members Post', form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)
