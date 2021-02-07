import mast
from flask import redirect, request, render_template, url_for, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from mast.users.forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm
from mast.models import User
from mast import bcr
from mast.tools.sis_authentication import authenticate_via_sis
from mast.tools.utils import check_profile_verified
from mast.session import Session

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
    session_data = Session()
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
                                              type=update_profile_form.type.data,
                                              uk_id=update_profile_form.uk_id.data.strip(),
                                              display_name=update_profile_form.display_name.data.strip(),
                                              anonymous=update_profile_form.anonymous.data)

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
        if key not in ['submit', 'csrf_token']:
            update_profile_form[key].data = current_user.__getattr__(key) or ''

    return render_template("user_settings.html", title='User Settings',
                           profile=current_user,
                           update_profile_form=update_profile_form,
                           display_update_profile_form=display_update_profile_form,
                           change_password_form=change_password_form,
                           display_change_password_form=display_change_password_form,
                           session_data=session_data)
