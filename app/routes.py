"""Initializaing the application instance."""
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
            UserPostForm, ContactForm, AdminLoginForm, AdminRegistrationForm, \
            AdminPostForm, PasswordResetRequestForm, PasswordResetForm, \
            UserPostEditForm, UserPostDeleteForm, UserMessageForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, UserPosts, Contacts, Admins, Posts, \
            UserMessages, Notifications
from werkzeug.urls import url_parse
from datetime import datetime
from app.email_sendgrid import email_password_reset


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Render the index/home page."""
    form = ContactForm()
    if form.validate_on_submit():
        info = Contacts(Name=form.name.data, Email=form.email.data,
                        Enquiry=form.enquiry.data)
        db.session.add(info)
        db.session.commit()
        flash('Enquiry sent successfully!!!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form)


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
        flash('Login successful')
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
                     Email=form.email.data)
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
    flash("Logged out successfully.")
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Render the user dashboard page."""
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.Timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('admin_post', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('admin_post', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('dashboard.html', title='Dashboard',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/profile/<Username>', methods=['GET', 'POST'])
@login_required
def profile(Username):
    """Render the user profile page."""
    user = Users.query.filter_by(Username=Username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = UserPosts.query.filter(user.UserID==UserPosts.UserID).order_by(UserPosts.Timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('profile', Username=user.Username, page=posts.next_num)\
        if posts.has_next else None
    prev_url = url_for('profile', Username=user.Username, page=posts.prev_num)\
        if posts.has_prev else None
    return render_template('profile.html', title='Profile', user=user,
                           posts=posts.items, next_url=next_url,
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
        return redirect(url_for('profile', Username=current_user.Username) )
    elif request.method == 'GET':
        form.username.data = current_user.Username
        form.bio.data = current_user.Bio
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.before_request
def before_request():
    """Render the date user login previously."""
    if current_user.is_authenticated:
        current_user.LastSeen = datetime.utcnow()
        db.session.commit()


@app.route('/members_post')
@login_required
def members_post():
    """Render the member post page."""
    page = request.args.get('page', 1, type=int)
    posts = UserPosts.query.order_by(UserPosts.Timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('members_post', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('members_post', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('members_post.html', title='Members Post',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
    """Render the password reset request page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(Email=form.email.data).first()
        if user:
            email_password_reset(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('password_reset_request.html',
                           title='Reset Password Request', form=form)


@app.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """Render the password reset page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = Users.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('password_reset.html',
                           title='Reset Password', form=form)


@app.route('/codeofconduct')
@login_required
def codeofconduct():
    """Render the code of conduct page."""
    return render_template('codeofconduct.html', title='STEC Code of Conduct')


@app.route('/yourposts/<Username>', methods=['GET', 'POST'])
@login_required
def yourposts(Username):
    """Render the current user post page."""
    form = UserPostForm()
    # editform = UserPostEditForm()

    if form.validate_on_submit():
        post = UserPosts(Body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post upload successful')
        return redirect(url_for('members_post'))

    user = Users.query.filter_by(Username=Username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = UserPosts.query.filter(user.UserID == UserPosts.UserID).order_by(
                                   UserPosts.Timestamp.desc()).paginate(
                                   page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('profile', Username=user.Username, page=posts.next_num)\
        if posts.has_next else None
    prev_url = url_for('profile', Username=user.Username, page=posts.prev_num)\
        if posts.has_prev else None
    return render_template('yourposts.html', title='Your Post page', user=user,
                           posts=posts.items, next_url=next_url, form=form,
                           prev_url=prev_url)


@app.route('/edit_post/<UserPostID>', methods=['GET', 'POST'])
@login_required
def edit_post(UserPostID):
    """Render user post edit page."""
    form = UserPostEditForm()
    post = UserPosts.query.filter_by(UserPostID=UserPostID).first_or_404()
    if form.validate_on_submit():
        post.Body = form.body.data
        db.session.commit()
        flash('Post updated.')
        return redirect(url_for('yourposts', Username=current_user.Username))
    elif request.method == 'GET':
        form.body.data = post.Body
    return render_template('edit_post.html', title='Edit Post',
                           form=form, post=post)


@app.route('/delete_post/<UserPostID>', methods=['GET', 'POST'])
@login_required
def delete_post(UserPostID):
    """Render user post edit page."""
    form = UserPostDeleteForm()
    post = UserPosts.query.filter_by(UserPostID=UserPostID).first_or_404()
    if form.validate_on_submit():
        post.Body = form.body.data
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted.')
        return redirect(url_for('yourposts', Username=current_user.Username))
    elif request.method == 'GET':
        form.body.data = post.Body

    return render_template('delete_post.html', title='Delete Post',
                           form=form, post=post)


@app.route('/private_message/<receiver>', methods=['GET', 'POST'])
@login_required
def private_message(receiver):
    """Render private message page."""
    user = Users.query.filter_by(Username=receiver).first_or_404()
    form = UserMessageForm()
    if form.validate_on_submit():
        msg = UserMessages(author=current_user, receiver=user,
                           Body=form.message.data)
        user.add_notification('unread_message', user.new_messages())
        db.session.add(msg)
        db.session.commit()
        flash('Message sent successfully.')
        return redirect(url_for('profile', Username=receiver))
    return render_template('private_message.html', title='Private Message',
                           form=form, receiver=receiver)


@app.route('/view_messages')
@login_required
def view_messages():
    """Render view message page."""
    current_user.LastMessageReadTime = datetime.utcnow()
    current_user.add_notification('unread_message', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.MessageReceived.order_by(
        UserMessages.Timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('view_messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('view_messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('view_messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/notifications')
@login_required
def notifications():
    """Render Notifications page."""
    since = request.args.get('since', 0.0, type=float)
    notices = current_user.Notification.filter(
        Notifications.Timestamp > since).order_by(Notifications.Timestamp.asc())
    return jsonify([{
        'Name': notice.Name,
        'Data': notice.get_data(),
        'Timestamp': notice.Timestamp
    } for notice in notices])


# # Adminstrator routes starts here
# @app.route('/admin_login', methods=['GET', 'POST'])
# def admin_login():
#     """Render the Sign in page."""
#     # To redirect authenticated/logged in admins
#     if current_user.is_authenticated:
#         return redirect(url_for('admin_dashboard'))
#     form = AdminLoginForm()
#     if form.validate_on_submit():
#         # Query database to check admin credentials
#         admin = Admins.query.filter_by(Username=form.username.data).first()
#         if admin is None or not admin.check_password(form.password.data):
#             # Redirect if admin credentials is incorrect
#             flash('Invalid username or password')
#             return redirect(url_for('admin_login'))
#         login_user(admin, remember=form.remember_me.data)
#         # Redirect if admin credentials is correct
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('admin_dashboard')
#         return redirect(next_page)
#     return render_template('admin_login.html', title='Admin Sign in',
#                            form=form)
#
#
# @app.route('/admin_register', methods=['GET', 'POST'])
# def admin_register():
#     """Render the registration page."""
#     # To redirect authenticated/logged in admins
#     if current_user.is_authenticated:
#         return redirect(url_for('admin_dashboard'))
#     form = AdminRegistrationForm()
#     if form.validate_on_submit():
#         admin = Admins(Name=form.name.data, Username=form.username.data,
#                        Email=form.email.data)
#         admin.set_password(form.password.data)
#         db.session.add(admin)
#         db.session.commit()
#         flash('Congratulations, you are an adminstrator of STEC!!!')
#         return redirect(url_for('admin_login'))
#     return render_template('admin_register.html', title='Admin Register',
#                            form=form)
#
#
# @app.route('/admin_logout')
# def admin_logout():
#     """To logout."""
#     logout_user()
#     return redirect(url_for('admin_login'))
#
#
# @app.route('/admin_dashboard', methods=['GET', 'POST'])
# @login_required
# def admin_dashboard():
#     """Render the user dashboard page."""
#     page = request.args.get('page', 1, type=int)
#     posts = Posts.query.order_by(Posts.Timestamp.desc()).paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('admin_post', page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('admin_post', page=posts.prev_num) \
#         if posts.has_prev else None
#
#     return render_template('admin_dashboard.html', title='Admin Dashboard',
#                            posts=posts.items, next_url=next_url,
#                            prev_url=prev_url)
#
#
# @app.route('/admin_post', methods=['GET', 'POST'])
# @login_required
# def admin_post():
#     """Render the member post page."""
#     form = AdminPostForm()
#     if form.validate_on_submit():
#         post = Posts(Subject=form.subject.data, Body=form.body.data,
#                      author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Post upload successfully')
#         return redirect(url_for('admin_post'))
#     return render_template('admin_post.html', title='Adminstrator Post',
#                            form=form)
#
#
# @app.route('/admin_enquiry', methods=['GET', 'POST'])
# @login_required
# def admin_enquiry():
#     """Render the member post page."""
#     page = request.args.get('page', 1, type=int)
#     enquiries = Contacts.query.order_by(Contacts.Timestamp.desc()).paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('admin_enquiry', page=enquiries.next_num) \
#         if enquiries.has_next else None
#     prev_url = url_for('admin_enquiry', page=enquiries.prev_num) \
#         if enquiries.has_prev else None
#
#     return render_template('admin_enquiry.html', title='User Enquiry',
#                            enquiries=enquiries.items, next_url=next_url,
#                            prev_url=prev_url)
