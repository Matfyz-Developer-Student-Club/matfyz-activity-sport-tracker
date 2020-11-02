from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD

app = Flask(__name__)
app.config['SECRET_KEY'] = '8e32c05c0914f857f3cadce4aff1cdd0'
=======
from flask_wtf.csrf import CSRFProtect
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = '8e32c05c0914f857f3cadce4aff1cdd0'
csrf = CSRFProtect(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

>>>>>>> 6fae7b0a1f13de702f3a40e3eecc45c5a93fd182
# TODO: Uncomment when database will be prepared
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
# bcr = Bcrypt(app)

# TODO: Uncomment when database will be prepared
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from mast import views