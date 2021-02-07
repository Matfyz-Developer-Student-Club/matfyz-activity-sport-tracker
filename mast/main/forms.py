from pathlib import Path
from typing import Dict, Any, Callable

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import logging
from mast.models import User
from flask_login import current_user
from mast.users.forms import LoggingFlaskForm


class CreditsForm(LoggingFlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Display')


class AddActivityForm(LoggingFlaskForm):
    activity = RadioField('Activity', validators=[DataRequired()], choices=['Walk', 'Run', 'Ride'])
    file = FileField('GPX file', validators=[FileRequired()], render_kw={'accept': '.xml,.gpx'})
    submit = SubmitField('Add activity')

    def validate_file(self, file):
        filename = secure_filename(file.data.filename)
        if filename == "":
            raise ValidationError("Provided file has invalid filename.")
        if Path(filename).suffix.lower() not in ['.gpx', '.xml']:
            raise ValidationError("Forbidden extension. Allowed extensions: '.gpx', '.xml'")
