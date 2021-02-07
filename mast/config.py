import os
from mast.tools.processor import GPXProcessor


class Config:
    SECRET_KEY = os.urandom(24)
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') if os.getenv(
        'SQLALCHEMY_DATABASE_URI') else 'sqlite:///site.db'
    UPLOAD_FILE_DIR = 'landing'
    PROCESSOR = GPXProcessor()
