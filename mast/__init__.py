from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['CSRF_ENABLED'] = True
csrf = CSRFProtect(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcr = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mast import views_pages, views_endpoints
