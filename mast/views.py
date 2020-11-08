from flask import redirect, request, render_template, url_for, jsonify
from mast import app
from mast.forms import LoginForm, RegisterForm, UpdateProfile, ChangePassword
from mast.models import UserMockup, Profile
import json
import datetime

_DAY_IN_WEEKS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

# Mockups for User settings
verified_profile = Profile("jon.doe@example.com")
verified_profile.verify_profile(first_name='Jon', last_name='Doe', age=18, sex='male', employee=False, nickname='JD')
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
    return render_template("personal_dashboard.html", title='Home', value_t=20)


@app.route('/global_dashboard')
def global_dashboard():
    return render_template("global_dashboard.html", title='Global Dashboard')


@app.route('/ten_km_contest')
def ten_km_contest():
    return render_template("running_10_km.html")


@app.route('/running_10_km')
def running_ten_km():
    global_data = [
        0,
        0,
        0,
    ]
    # TODO: replace with data from query - personal data of a concrete user
    personal_data = [
        1,
        1,
        2,
    ]
    # TODO: replace with corresponding labels from querry - 5 km  ??? maybe not necessary
    labels = [
        '43',
        '44',
        '45',
    ]

    return jsonify(
        {'payload': json.dumps({'global_data': global_data, 'personal_data': personal_data, 'labels': labels})})


@app.route('/get_personal_stats')
def get_personal_stats():
    today = datetime.datetime.now()
    labels = [_DAY_IN_WEEKS[(day - 1) % 7] + ' ' + today.date().strftime("%x") for day in
              range(today.day, today.day + 7)]
    # TODO: get current_user db snapshot for last period
    data = [12, 19, 3, 5, 2, 3, 7]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


@app.route('/get_global_contest_foot')
def get_global_contest_foot():
    labels = ["Where we gonna make it on foot."]
    data = [425]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


@app.route('/get_global_contest_bike')
def get_global_contest_bike():
    labels = ["Where we gonna make it by bike."]
    data = [211]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


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
