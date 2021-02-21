import mast
import requests
import logging
from flask import redirect, request, render_template, url_for, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from mast.users.forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm
from mast.models import User
from mast import bcr
from mast.tools.sis_authentication import authenticate_via_sis
from mast.tools.utils import check_profile_verified
from mast.session import Session
from mast.tools.STRAVA_authentication import *

users = Blueprint('users', __name__)


@users.route('/', methods=['GET', 'POST'])
@users.route('/')
@users.route('/welcome')
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        form = LoginForm()
        return render_template('welcome.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and bcr.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('main.home'))
            else:
                form.email.errors.append(
                    'Specified pair of email and password is invalid!')
    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form = RegisterForm('register_form')
        return render_template('register.html', title='Registration', form=form)
    else:
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            hashed_password = bcr.generate_password_hash(
                form.password.data.strip()).decode('UTF-8')
            user = User(email=form.email.data.lower().strip(),
                        password=hashed_password)
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            return render_template('register.html', title='Registration', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    session_data = mast.session.Session()
    update_profile_form = UpdateProfileForm(name='up')
    display_update_profile_form = 'none'
    change_password_form = ChangePasswordForm(name='chp')
    display_change_password_form = 'none'
    if request.method == 'POST':
        if request.form['submit'] == 'Update profile':
            update_profile_form = UpdateProfileForm(request.form)
            if update_profile_form.validate():
                current_user.complete_profile(first_name=update_profile_form.first_name.data.strip(),
                                              last_name=update_profile_form.last_name.data.strip(),
                                              age=update_profile_form.age.data,
                                              sex=update_profile_form.sex.data,
                                              shirt_size=update_profile_form.shirt_size.data,
                                              user_type=update_profile_form.user_type.data,
                                              ukco=update_profile_form.ukco.data.strip(),
                                              display_name=update_profile_form.display_name.data.strip(),
                                              anonymous=update_profile_form.competing.data)

                if authenticate_via_sis(name=current_user.first_name, surname=current_user.last_name, login=None,
                                        uk_id=current_user.uk_id, is_employee=current_user.type.value):
                    current_user.verify()
                    session_data.info('Your profile has been been verified.')
                    return redirect(url_for('users.user_settings'))
                else:
                    session_data.warning('Your profile has not been been verified.<br />' +
                                         'We will verify your profile in a few days if you are sure with your data.')

            else:
                # Keep the form visible if it contains errors
                display_update_profile_form = 'block'
        elif request.form['submit'] == 'Update password':
            change_password_form = ChangePasswordForm(request.form)
            if change_password_form.validate():
                hashed_password = bcr.generate_password_hash(
                    change_password_form.password.data).decode('UTF-8')
                current_user.change_password(hashed_password)
                session_data.info('Your password has been changed.')
                return redirect(url_for('users.user_settings'))
            else:
                # Keep the form visible if it contains errors
                display_change_password_form = 'block'

    # For GET and after POST method
    check_profile_verified(session_data)

    for key, data in update_profile_form.data.items():
        if key in ["first_name", "last_name", "display_name"]:
            update_profile_form[key].data = current_user.__getattr__(key) or ''

    update_profile_form.ukco.data = current_user.uk_id or ''
    update_profile_form.age.data = current_user.age.value if current_user.age else None
    update_profile_form.sex.data = current_user.sex.value if current_user.sex else None
    update_profile_form.shirt_size.data = current_user.shirt_size or None
    update_profile_form.user_type.data = current_user.type.value if current_user.type else None
    update_profile_form.competing.data = current_user.anonymous or None

    return render_template("user_settings.html", title='User Settings',
                           profile=current_user,
                           update_profile_form=update_profile_form,
                           display_update_profile_form=display_update_profile_form,
                           change_password_form=change_password_form,
                           display_change_password_form=display_change_password_form,
                           session_data=session_data)


STRAVA_CLIENT_ID = 61623
STRAVA_CLIENT_SECRET = '71af3bcd89c9a583607db1a383e36f8c1cf6790a' 

@users.route('/strava', methods=['GET', 'POST'])
@login_required
def strava():    
    scope = "read_all,activity:read"
    return redirect(f"http://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&response_type=code&redirect_uri=http://localhost:5000/strava/auth&approval_prompt=force&scope={scope}")

@users.route('/strava/auth', methods=['GET'])
@login_required
def strava_auth():
    # request = "GET /strava/auth?state=&code=2db1b5fbcc4aae3815caf2988a4ae871592912d8&scope=read,read_all HTTP/1.1"
    # TODO: inspect request code and scope
    # if scope is not valid then display error msg
    code = request.args.get('code')
    scope = request.args.get('scope')

    if not check_strava_permissions(scope):
        #TODO: tell user to fuck off
        # return to page that tells user to fuck off
        return "nonono"

    logging.info("CODE: " + code)
    logging.info("SCOPE: " + scope)
    save_strava_tokens(code)
    #get_activities()
    return 'hello'

    