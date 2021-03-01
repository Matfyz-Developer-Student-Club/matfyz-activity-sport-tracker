import os
from mast.tools.processor import GPXProcessor


class Config:
    SECRET_KEY = os.urandom(24)
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') if os.getenv(
        'SQLALCHEMY_DATABASE_URI') else 'sqlite:///site.db'
    UPLOAD_FILE_DIR = '../landing'
    PROCESSOR = GPXProcessor()
    LANDING_DIR = 'landing'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
