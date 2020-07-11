"""Importing os."""
import os
import pymysql
import dbinfo
basedir = os.path.abspath(os.path.dirname(__file__))

dblink = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(
    dbinfo.user, dbinfo.dbpass, dbinfo.host, dbinfo.dbname)


class Config(object):
    """Configuration credentials."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'stec-web-developed'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or dblink
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # For email confirmation
    SECURITY_PASSWORD_SALT = 'stec-email-confirmation-formembers'

    # No to show before Pagination
    POSTS_PER_PAGE = 2

    # sendgrid mail configuations
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    # remember to add sendgrid key and default sender
    MAIL_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # heroku log
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
