"""SendGrid Configuration."""
from flask import render_template
from flask_mail import Message
from app import mail, app
from config import Config

# sender = app.config['MAIL_DEFAULT_SENDER']

def send_email(subject, sender, recipients, text_body, html_body):
    """Email information."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


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
