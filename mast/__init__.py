from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
import logging
from mast.config import Config
import os

db = SQLAlchemy()
bcr = Bcrypt()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def create_app(configuration=Config):
    app = Flask(__name__)
    app.config.from_object(configuration)

    mail.init_app(app)
    db.init_app(app)
    bcr.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    logging.info(f"{app.config['SQLALCHEMY_DATABASE_URI']}")
    logging.info(f"{os.getenv('DATABASE_URL')}")

    # Logging setup
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f"{app.config['STRAVA_CLIENT_ID']}")
    from mast.users.routes import users
    from mast.activities.routes import activities
    from mast.main.routes import main
    from mast.views.routes import views
    from mast.integrations.routes import integrations

    app.register_blueprint(users)
    app.register_blueprint(activities)
    app.register_blueprint(main)
    app.register_blueprint(views)
    app.register_blueprint(integrations)

    return app
