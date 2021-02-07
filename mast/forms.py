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

## Logging setup
form_logger = logging.getLogger('form_submission')

## Frontend from validation with html attributes
# combine to kw_arguments argument of Field
# email pattern from https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/email#Basic_validation
min_length_attribute: Callable[[int], Dict[str, Any]] = lambda n: {'minlength': n.__str__()}
max_length_attribute: Callable[[int], Dict[str, Any]] = lambda n: {'maxlength': n.__str__()}




