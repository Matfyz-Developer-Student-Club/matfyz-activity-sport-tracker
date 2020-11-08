import os

from flask import redirect, request, render_template, url_for
from werkzeug.utils import secure_filename

from mast import app
from mast.forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm, AddActivityForm
from mast.models import User
from mast import db

UPLOAD_FILE_DIR = 'landing'

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)
        if form.validate():
            # TODO: redirect the user to main page
            return redirect(url_for('home'))
        else:
            return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm('register_form')
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(request.form)
        if form.validate():
            # TODO: add user to database
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)


@app.route('/personal_dashboard', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    add_activity_form = AddActivityForm()
    print(request.form)
    if add_activity_form.validate_on_submit():
        # TODO: validate uploaded file
        # TODO: add the record to the database
        print('Validated')
        filename = secure_filename(add_activity_form.file.data.filename)
        add_activity_form.file.data.save(os.path.join(UPLOAD_FILE_DIR, filename))
    return render_template("personal_dashboard.html", title='Home', form=add_activity_form)


@app.route('/global_dashboard')
def global_dashboard():
    return render_template("global_dashboard.html", title='Global Dashboard')


@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    # TODO: Mockups for User settings - user #1
    user = db.session.query(User).get(1)

    update_profile_form = UpdateProfileForm(name='up')
    display_update_profile_form = 'none'
    change_password_form = ChangePasswordForm(name='chp')
    display_change_password_form = 'none'
    if request.method == 'POST':
        if request.form['submit'] == 'Update profile':
            update_profile_form = UpdateProfileForm(request.form)
            if update_profile_form.validate():
                # TODO: validate the form based on db
                # TODO: update the data in the db
                # TODO delete next later
                user.verify()
            else:
                # Keep the form visible if it contains errors
                display_update_profile_form = 'block'
        elif request.form['submit'] == 'Change password':
            change_password_form = ChangePasswordForm(request.form)
            if change_password_form.validate():
                # TODO: update db
                pass
            else:
                # Keep the form visible if it contains errors
                display_change_password_form = 'block'

    # For GET and after POST method
    return render_template("user_settings.html", title='User Settings',
                           profile=user,
                           update_profile_form=update_profile_form,
                           display_update_profile_form=display_update_profile_form,
                           change_password_form=change_password_form,
                           display_change_password_form=display_change_password_form,
                           )


@app.route('/integrations')
def integrations():
    return render_template("integrations.html", title='Integrations')
  
