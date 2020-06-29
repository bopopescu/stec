"""Importing os."""
import os
import pymysql
import dbinfo
basedir = os.path.abspath(os.path.dirname(__file__))

dblink = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(dbinfo.user, dbinfo.dbpass, dbinfo.host, dbinfo.dbname)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'stec-web-developed'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or dblink
    SQLALCHEMY_TRACK_MODIFICATIONS = False
