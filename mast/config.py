import os
from mast.tools.processor import GPXProcessor


class Config:
    SECRET_KEY = os.urandom(24)
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    UPLOAD_FILE_DIR = '../landing'
    PROCESSOR = GPXProcessor()
    LANDING_DIR = 'landing'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
    STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
    STRAVA_SCOPE = ['activity:read']
    STRAVA_EXPIRE_RESERVE = 1000
    #TODO: not working on local with this field
    SERVER_NAME = 'mathletics-test.ks.matfyz.cz'
