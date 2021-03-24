from typing import Dict, Any, Callable

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import logging
from mast.models import User

## Logging setup
form_logger = logging.getLogger('form_submission')

## Frontend from validation with html attributes
# combine to kw_arguments argument of Field
# email pattern from https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/email#Basic_validation
min_length_attribute: Callable[[int], Dict[str, Any]] = lambda n: {'minlength': n.__str__()}
max_length_attribute: Callable[[int], Dict[str, Any]] = lambda n: {'maxlength': n.__str__()}

PASSWORD_MIN_LEN = 8
PASSWORD_MAX_LEN = 50


def log_form_submit(form):
    form_logger.info(f'Received {type(form)}')
    has_error = False
    for field in form:
        if field.errors:
            has_error = True
            form_logger.error(f'FIELD[{field.label.text}] - ERRORS{field.errors} - VALUE["{field.data}"]')
    if not has_error:
        form_logger.info('Form OK')
    else:
        form_logger.error('From contained Errors!')


class LoggingFlaskForm(FlaskForm):
    def validate(self):
        res = super().validate()
        log_form_submit(self)
        return res


class RegisterForm(LoggingFlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)],
                             render_kw={**min_length_attribute(PASSWORD_MIN_LEN),
                                        **max_length_attribute(PASSWORD_MAX_LEN)})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create an account')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data.lower()).first()
        if user_email:
            raise ValidationError(f'Email {email.data} is already in use!')


class LoginForm(LoggingFlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(LoggingFlaskForm):
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(min=2, max=50)],
                             render_kw={**min_length_attribute(2), **max_length_attribute(50)})
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw={**min_length_attribute(2), **max_length_attribute(50)})
    display_name = StringField('Display name', validators=[Length(0, 50)],
                               render_kw={**min_length_attribute(2), **max_length_attribute(50)},
                               description='Optional name to show on the scoreboards.')
    ukco = StringField('UKČO', validators=[DataRequired(), Length(min=8, max=8)],
                       render_kw={**min_length_attribute(8), **max_length_attribute(8)})
    sex = RadioField('Sex', validators=[DataRequired()], choices=['male', 'female'])
    shirt_size = RadioField('Shirt size', validators=[DataRequired()], choices=['S', 'M', 'L', 'XL', 'XXL'])
    user_type = RadioField('I am', validators=[DataRequired()],
                           choices=['student', 'employee', 'alumni'])
    study_field = RadioField('I study', validators=[DataRequired()],
                             choices=['Informatics', 'Maths', 'Physics', 'Teaching'])
    anonymous = BooleanField('I want to compete anonymously',
                             description='Results will be on the public scoreboards without name.')
    competing = BooleanField('I want to compete',
                             description='Results will be included in the common challenges.')
    submit = SubmitField('Update profile')


class ChangePasswordForm(LoggingFlaskForm):
    password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=50)],
                             render_kw={**min_length_attribute(8), **max_length_attribute(50)})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update password')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f"There is no account with email: '{email.data}'. Please Sign-Up!")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)],
                             render_kw={**min_length_attribute(PASSWORD_MIN_LEN),
                                        **max_length_attribute(PASSWORD_MAX_LEN)})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
