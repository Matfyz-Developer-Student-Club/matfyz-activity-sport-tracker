from flask import redirect, request, render_template, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from mast.forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm
from mast.models import User
import mast.queries
import json
import datetime
from mast import db, app, bcr

_DAY_IN_WEEKS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday',
                 'Thursday', 'Friday', 'Saturday')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcr.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')

                if next_page:
                    redirect(next_page)
                else:
                    return redirect(url_for('home'))
        # TODO: Inform user about incorrect passwd
        return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm('register_form')
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            hashed_password = bcr.generate_password_hash(form.password.data).decode('UTF-8')
            user = User(email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/personal_dashboard')
@app.route('/home')
@login_required
def home():
    session = mast.queries.Queries()
    last_activities = session.get_user_last_activities(current_user.id, 10)
    last_activities = [] if not last_activities else last_activities
    return render_template("personal_dashboard.html", title='Home', last_activities=last_activities)


@app.route('/global_dashboard')
@login_required
def global_dashboard():
    return render_template("global_dashboard.html", title='Global Dashboard')


@app.route('/get_global_contest')
@login_required
def get_global_contest():
    session = mast.queries.Queries()
    labels = ["Where we gonna make it by bike.", "Where we gonna make it on foot."]
    data = session.get_global_total_distance_on_bike()
    # checkpoints = session.get_challenge_parts()
    checkpoints = {'a': 2, 'b': 3}
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels, 'checkpoints': checkpoints})})



@app.route('/running_5_km')
@login_required
def running_5_km():
    # TODO: replace with data from query
    items = []
    for i in range(6):
        item = dict(date="2020-03-" + str(i), id=i, distance=i, time=i * 6)
        items.append(item)
    return render_template("running_5_km.html", items=items)


@app.route('/get_running_5_km')
@login_required
def get_running_5_km():
    # TODO: replace with data from query - data of all users
    return jsonify(
        {'payload': json.dumps({'global_data': global_data, 'personal_data': personal_data, 'labels': labels})})


@app.route('/running_10_km')
@login_required
def running_10_km():
    items = []
    for i in range(6):
        item = dict(date="2020-03-" + str(i), id=i, distance=i, time=i * 6)
        items.append(item)
    return render_template("running_10_km.html", items=items)


@app.route('/get_running_10_km')
@login_required
def get_running_10_km():
    # TODO: replace with data from query - data of all users
    return jsonify(
        {'payload': json.dumps({'global_data': global_data, 'personal_data': personal_data, 'labels': labels})})


@app.route('/running_jogging')
@login_required
def running_jogging():
    return render_template("running_jogging.html")


@app.route('/get_running_jogging')
@login_required
def get_running_jogging():
    # TODO: replace with data from query - personal data of a concrete user
    personal_data = [
        0,
        1,
        1,
        2,
        2,
        3,
        3,
    ]
    # TODO: replace with corresponding labels from querry - 5 km  ??? maybe not necessary
    labels = ['Monday', 'Tuesday', 'Wednesday',
              'Thursday', 'Friday', 'Saturday', 'Sunday']

    return jsonify({'payload': json.dumps({'personal_data': personal_data, 'labels': labels})})


@app.route('/get_personal_stats')
@login_required
def get_personal_stats():
    today = datetime.datetime.now()
    labels = [_DAY_IN_WEEKS[(day - 1) % 7] + ' ' + today.date().strftime("%x") for day in
              range(today.day, today.day + 7)]
    # TODO: get current_user db snapshot for last period
    data = [12, 19, 3, 5, 2, 3, 7]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


@app.route('/user_settings', methods=['GET', 'POST'])
@login_required
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


@app.route('/cycling')
@login_required
def cycling():
    return render_template("cycling.html")


@app.route('/integrations')
@login_required
def integrations():
    return render_template("integrations.html", title='Integrations')
