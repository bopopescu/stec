"""SendGrid Configuration."""
from flask import render_template
from flask_mail import Message
from app import mail, app
from config import Config
from threading import Thread
from itsdangerous import URLSafeTimedSerializer

sender = app.config['MAIL_DEFAULT_SENDER']

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    """Email information."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def email_password_reset(user):
    """Password reset email information."""
    token = user.get_reset_password_token()
    send_email('[STEC] Reset Your Password',
               sender=sender,
               recipients=[user.Email],
               text_body=render_template('email/password_reset.txt',
                                         user=user, token=token),
               html_body=render_template('email/password_reset.html',
                                         user=user, token=token))

def email_confirmation(user):
    """Email confirmation information."""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    emailToken = serializer.dumps(user.Email, salt=app.config['SECURITY_PASSWORD_SALT'])
    send_email('[STEC] Email Confirmation',
               sender=sender,
               recipients=[user.Email],
               text_body=render_template('email/email_confirmation.txt',
                                         user=user, emailToken=emailToken),
               html_body=render_template('email/email_confirmation.html',
                                         user=user, emailToken=emailToken))
