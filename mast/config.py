import os


class Config:
    SECRET_KEY = os.urandom(24)
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
    STRAVA_SCOPE = ['activity:read']
    STRAVA_EXPIRE_RESERVE = 1000
    # TODO: not working on local with this field
    SERVER_NAME = 'mathletics.mff.cuni.cz'
    SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
