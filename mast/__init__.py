from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging
from mast.config import Config

db = SQLAlchemy()
bcr = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(configuration=Config):
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)
    bcr.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Logging setup
    logging.basicConfig(level=logging.DEBUG)

    from mast.users.routes import users
    from mast.activities.routes import activities
    from mast.main.routes import main
    from mast.views.routes import views

    app.register_blueprint(users)
    app.register_blueprint(activities)
    app.register_blueprint(main)
    app.register_blueprint(views)

    return app
