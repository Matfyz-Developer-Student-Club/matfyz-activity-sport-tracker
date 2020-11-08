from flask import redirect, request, render_template, url_for, jsonify
from mast.forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm
from mast import app
from mast.models import User
from mast import db
import json
import datetime

_DAY_IN_WEEKS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday',
                 'Thursday', 'Friday', 'Saturday')

@app.route('/', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)
        if form.validate():
            # TODO: redirect the user to main page
            return render_template("personal_dashboard.html", title='Home')
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

@app.route('/running_5_km')
def running_5_km():
    # TODO: replace with data from query
    items = []
    for i in range(6):
        item = dict(date="2020-03-" + str(i), id=i, distance=i, time=i*6)
        items.append(item)
    return render_template("running_5_km.html", items=items)


@app.route('/get_running_5_km')
def get_running_5_km():
    # TODO: replace with data from query - data of all users
    global_data = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        2,
        2,
        4,
        3,
        4,
        5,
        2,
        3,
        5,
        0,
        0,
        0,
        0,
        0,
        0,
        0, ]
    # TODO: replace with data from query - personal data of a concrete user
    personal_data = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        2,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0, ]
    # TODO: replace with corresponding labels from querry - 5 km  ??? maybe not necessary
    labels = [
        '20',
        '21',
        '22',
        '23',
        '24',
        '25',
        '26',
        '27',
        '28',
        '29',
        '30',
        '31',
        '32',
        '33',
        '34',
        '35',
        '36',
        '37',
        '38',
        '39',
        '41',
        '42',
        '43',
        '44',
        '45',
    ]

    return jsonify({'payload': json.dumps({'global_data': global_data, 'personal_data': personal_data, 'labels': labels})})


@app.route('/running_10_km')
def running_10_km():
    items = []
    for i in range(6):
        item = dict(date="2020-03-" + str(i), id=i, distance=i, time=i*6)
        items.append(item)
    return render_template("running_10_km.html", items=items)


@app.route('/get_running_10_km')
def get_running_10_km():
    # TODO: replace with data from query - data of all users
    global_data = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0, ]
    # TODO: replace with data from query - personal data of a concrete user
    personal_data = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        2,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0, ]
    # TODO: replace with corresponding labels from querry - 5 km  ??? maybe not necessary
    labels = [
        '20',
        '21',
        '22',
        '23',
        '24',
        '25',
        '26',
        '27',
        '28',
        '29',
        '30',
        '31',
        '32',
        '33',
        '34',
        '35',
        '36',
        '37',
        '38',
        '39',
        '41',
        '42',
        '43',
        '44',
        '45',
    ]

    return jsonify(
        {'payload': json.dumps({'global_data': global_data, 'personal_data': personal_data, 'labels': labels})})


@app.route('/running_jogging')
def running_jogging():
    items = []
    for i in range(6):
        item = dict(date="2020-03-" + str(i), id=i, distance=i, time=i*6)
        items.append(item)
    return render_template("running_jogging.html", items=items)


@app.route('/get_running_jogging')
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


@app.route('/cycling')
def cycling():
    # TODO: replace with data from query
    items = []
    for i in range(6):
        item = dict(date="2020-03-" + str(i), id=i, distance=i, time=i*6)
        items.append(item)
    return render_template("cycling.html", items=items)


@app.route('/get_cycling')
def get_cycling():

    # TODO: replace with data from query - personal data of a concrete user
    personal_data = [
        0,
        1,
        3,
        2,
        2,
        3,
        1,
    ]
    # TODO: replace with corresponding labels from querry - 5 km  ??? maybe not necessary
    labels = ['Monday', 'Tuesday', 'Wednesday',
              'Thursday', 'Friday', 'Saturday', 'Sunday']

    return jsonify({'payload': json.dumps({'personal_data': personal_data, 'labels': labels})})

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


@app.route('/running_5_km')
def running_5_km():
    return render_template("running_5_km.html", title='Running - 5 km')


@app.route('/running_10_km')
def running_10_km():
    return render_template("running_10_km.html", title='Running - 10 km')


@app.route('/running_jogging')
def running_jogging():
    return render_template("running_jogging.html", title='Running / Jogging')
