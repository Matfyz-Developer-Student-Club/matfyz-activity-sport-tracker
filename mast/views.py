from flask import redirect, request, render_template, url_for
from mast import app
from mast.forms import LoginForm, RegisterForm, UpdateProfile, ChangePassword
from mast.models import UserMockup, Profile

# Mockups for User settings
verified_profile = Profile("jon.doe@example.com")
verified_profile.complete_profile(first_name='Jon', last_name='Doe', age='<=35', sex='male', shirt_size='M', competing=True,
                                  employee=True, display_name='JD')
unverified_profile = Profile("alice@example.com")
user = UserMockup(unverified_profile)


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


@app.route('/personal_dashboard')
@app.route('/home')
def home():
    return render_template("personal_dashboard.html", title='Home')


@app.route('/global_dashboard')
def global_dashboard():
    return render_template("global_dashboard.html", title='Global Dashboard')


@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    update_profile_form = UpdateProfile(name='up')
    display_update_profile_form = 'none'
    change_password_form = ChangePassword(name='chp')
    display_change_password_form = 'none'
    if request.method == 'POST':
        if request.form['submit'] == 'Update profile':
            update_profile_form = UpdateProfile(request.form)
            if update_profile_form.validate():
                # TODO: validate the form based on db
                # TODO: update the data in the db
                # TODO delete next later
                user.profile = verified_profile
            else:
                # Keep the form visible if it contains errors
                display_update_profile_form = 'block'
        elif request.form['submit'] == 'Change password':
            change_password_form = ChangePassword(request.form)
            if change_password_form.validate():
                # TODO: update db
                pass
            else:
                # Keep the form visible if it contains errors
                display_change_password_form = 'block'

    # For GET and after POST method
    return render_template("user_settings.html", title='User Settings',
                           profile=user.profile,
                           update_profile_form=update_profile_form,
                           display_update_profile_form=display_update_profile_form,
                           change_password_form=change_password_form,
                           display_change_password_form=display_change_password_form,
                           )


@app.route('/integrations')
def integrations():
    return render_template("integrations.html", title='Integrations')
  
