from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import logging

## Logging setup
form_logger = logging.getLogger('form_submission')


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
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create an account')


class LoginForm(LoggingFlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfile(LoggingFlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=50)])
    nickname = StringField('Nickname', validators=[Length(2,50)])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Sex', validators=[DataRequired()], choices=['male', 'female'])
    employee = BooleanField('Faculty employee', description='Does not apply to employed students.')
    submit = SubmitField('Update profile')


class ChangePassword(LoggingFlaskForm):
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update password')
