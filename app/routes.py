"""Initializaing the application instance."""
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify,\
                abort
from werkzeug.urls import url_parse
from itsdangerous import URLSafeTimedSerializer
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
            UserPostForm, ContactForm, AdminPostForm, \
            PasswordResetRequestForm, PasswordResetForm, \
            UserPostEditForm, UserPostDeleteForm, UserMessageForm, \
            AdminPostEditForm, AdminPostDeleteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, UserPosts, Contacts, Posts, \
            UserMessages, Notifications
from app.email_sendgrid import email_password_reset, email_confirmation, \
            email_confirmation_resend


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
        flash('Enquiry submitted successfully!!!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the Sign in page."""
    # To redirect authenticated/logged in user
    if current_user.is_authenticated and current_user.StecAdmin==True:
        return redirect(url_for('admin_dashboard'))
    elif current_user.is_authenticated:
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
        if next_page is None or not next_page.startswith('/'):
            next_page = url_for('dashboard')
        flash('Login successful')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Render the registration page."""
    # To redirect authenticated/logged in user
    if current_user.is_authenticated and current_user.StecAdmin==True:
        return redirect(url_for('admin_dashboard'))
    elif current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(Name=form.name.data, Username=form.username.data,
                     Email=form.email.data, Confirmed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        email_confirmation(user)
        flash('An email confirmation has been sent, check your email.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/confirm/<emailToken>', methods=['GET', 'POST'])
def confirm_email(emailToken):
    """Render the email confirmation page."""
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        Email = serializer.loads(emailToken,
                                 salt=app.config['SECURITY_PASSWORD_SALT'],
                                 max_age=1800)
    except:
        flash('The confirmation link is Invalid or has expired')

    user = Users.query.filter_by(Email=Email).first_or_404()

    user.Confirmed = True
    user.ConfirmedDate = datetime.utcnow()
    db.session.add(user)
    db.session.commit()

    flash('Email confirmation successful, Welcome to STEC!!!')
    return redirect(url_for('login'))


@app.before_request
def before_request():
    """Render the previous date the user logged in."""
    if current_user.is_authenticated:
        current_user.LastSeen = datetime.utcnow()
        db.session.commit()
    elif current_user.is_authenticated and not current_user.Confirmed:
        return redirect(url_for('email_unconfirmed'))


@app.route('/email_unconfirmed')
def email_unconfirmed():
    if current_user.is_authenticated and current_user.Confirmed==True:
        return redirect(url_for('dashboard'))
    elif not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('email_unconfirmed.html')


@app.route('/confirm')
@login_required
def resend_confirmation():
    email_confirmation_resend(current_user)
    flash('A new email confirmation has been sent, check your email.')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """To logout."""
    logout_user()
    flash("Log out successful.")
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
    """Render the user's profile page."""
    user = Users.query.filter_by(Username=Username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = UserPosts.query.filter(user.UserID==UserPosts.UserID).order_by(
                UserPosts.Timestamp.desc()).paginate(
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
        flash('Profile edit successful.')
        return redirect(url_for('profile', Username=current_user.Username))
    elif request.method == 'GET':
        form.username.data = current_user.Username
        form.bio.data = current_user.Bio
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.before_request
def before_request():
    """Render the previous date the user logged in."""
    if current_user.is_authenticated:
        current_user.LastSeen = datetime.utcnow()
        db.session.commit()


@app.route('/members_post')
@login_required
def members_post():
    """Render the member posts page."""
    page = request.args.get('page', 1, type=int)
    posts = UserPosts.query.order_by(UserPosts.Timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('members_post', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('members_post', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('members_post.html', title='Member Posts',
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
        flash('Check your email for the link to reset your password')
        return redirect(url_for('login'))
    return render_template('password_reset_request.html',
                           title='Password Reset Request', form=form)


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
        flash('password reset successful.')
        return redirect(url_for('login'))
    return render_template('password_reset.html',
                           title='Password Reset', form=form)


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
    return render_template('yourposts.html', title='Personal Post',
                           user=user, posts=posts.items, next_url=next_url,
                           form=form, prev_url=prev_url)


@app.route('/edit_post/<UserPostID>', methods=['GET', 'POST'])
@login_required
def edit_post(UserPostID):
    """Render user post edit page."""
    form = UserPostEditForm()
    post = UserPosts.query.filter_by(UserPostID=UserPostID).first_or_404()
    if form.validate_on_submit():
        post.Body = form.body.data
        db.session.commit()
        flash('Post updated')
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
        flash('Post Deleted')
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
        Notifications.Timestamp > since).order_by(
            Notifications.Timestamp.asc())
    return jsonify([{
        'Name': notice.Name,
        'Data': notice.get_data(),
        'Timestamp': notice.Timestamp
    } for notice in notices])


# Adminstrator routes starts here
@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    """Render the user dashboard page."""
    if current_user.StecAdmin==True:
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.order_by(Posts.Timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('admin_post', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('admin_post', page=posts.prev_num) \
            if posts.has_prev else None
        return render_template('admin_dashboard.html', title='Admin Dashboard',
                               posts=posts.items, next_url=next_url,
                               prev_url=prev_url)
    flash('You are not an administrator')
    return redirect(url_for('dashboard'))


@app.route('/admin_post', methods=['GET', 'POST'])
@login_required
def admin_post():
    """Render the member post page."""
    if current_user.StecAdmin==True:
        form = AdminPostForm()
        if form.validate_on_submit():
            post = Posts(Subject=form.subject.data, Body=form.body.data,
                         author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Post upload successfully')
            return redirect(url_for('admin_post'))
        return render_template('admin_post.html', title='New Article',
                               form=form)
    flash('You are not an administrator.')
    return redirect(url_for('dashboard'))

@app.route('/admin_enquiry', methods=['GET', 'POST'])
@login_required
def admin_enquiry():
    """Render the member post page."""
    if current_user.StecAdmin==True:
        current_user.LastEnquiryReadTime = datetime.utcnow()
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        enquiries = Contacts.query.order_by(Contacts.Timestamp.desc()
                                            ).paginate(page,
                                                       app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('admin_enquiry', page=enquiries.next_num) \
            if enquiries.has_next else None
        prev_url = url_for('admin_enquiry', page=enquiries.prev_num) \
            if enquiries.has_prev else None
        return render_template('admin_enquiry.html', title='User Enquiry',
                               enquiries=enquiries.items, next_url=next_url,
                               prev_url=prev_url)
    flash('You are not an administrator.')
    return redirect(url_for('dashboard'))


@app.route('/edit_article/<PostID>', methods=['GET', 'POST'])
@login_required
def edit_article(PostID):
    """Render Admin post edit page."""
    if current_user.StecAdmin==True:
        form = AdminPostEditForm()
        post = Posts.query.filter_by(PostID=PostID).first_or_404()
        if form.validate_on_submit():
            post.Subject = form.subject.data
            post.Body = form.body.data
            db.session.commit()
            flash('Article updated.')
            return redirect(url_for('admin_dashboard'))
        elif request.method == 'GET':
            form.subject.data = post.Subject
            form.body.data = post.Body
        return render_template('edit_article.html', title='Edit Article',
                               form=form, post=post)
    flash('You are not an administrator.')
    return redirect(url_for('dashboard'))


@app.route('/delete_article/<PostID>', methods=['GET', 'POST'])
@login_required
def delete_article(PostID):
    """Render Admin post edit page."""
    if current_user.StecAdmin==True:
        form = AdminPostDeleteForm()
        post = Posts.query.filter_by(PostID=PostID).first_or_404()
        if form.validate_on_submit():
            post.Subject = form.subject.data
            post.Body = form.body.data
            db.session.delete(post)
            db.session.commit()
            flash('Post Deleted.')
            return redirect(url_for('admin_dashboard'))
        elif request.method == 'GET':
            form.subject.data = post.Subject
            form.body.data = post.Body
        return render_template('delete_article.html', title='Delete Article',
                               form=form, post=post)
    flash('You are not an administrator.')
    return redirect(url_for('dashboard'))
