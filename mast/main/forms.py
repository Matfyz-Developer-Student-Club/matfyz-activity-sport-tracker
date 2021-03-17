from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
from wtforms import PasswordField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired, ValidationError
from mast.users.forms import LoggingFlaskForm
from pathlib import Path


# TODO: Add logging on file load

class CreditsForm(LoggingFlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Display')
    print()


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
