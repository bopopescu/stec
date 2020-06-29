"""Initializaing the application instance."""
from flask import Flask
import mysql.connector
import hashlib
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
dbconfig = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '8889',
    'raise_on_warnings': True,
    'database': 'STEC'
}
dblink = mysql.connector.connect(**dbconfig)
dblink.close()

from app import routes
