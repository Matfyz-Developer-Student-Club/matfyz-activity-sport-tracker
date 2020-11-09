import json
import os
import datetime
import mast
from flask import redirect, request, render_template, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from mast.forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm, AddActivityForm
from mast.models import User, Competition, Sex, Age, Activity, ActivityType
from mast import db, app, bcr, queries
from mast.tools.sis_authentication import authenticate_via_sis
from mast.processor import GPXProcessor

UPLOAD_FILE_DIR = 'landing'
PROCESSOR = GPXProcessor()


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
                return redirect(url_for('home'))
            else:
                form.email.errors.append('Your username or password is invalid!')
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


@app.route('/personal_dashboard', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    session = mast.queries.Queries()
    last_activities = session.get_user_last_activities(current_user.id, 10)
    last_activities = [] if not last_activities else last_activities
    add_activity_form = AddActivityForm()
    if add_activity_form.validate_on_submit():
        # TODO: validate uploaded file
        # TODO: add the record to the database
        filename = secure_filename(add_activity_form.file.data.filename)
        path = os.path.join(__file__, os.pardir)
        add_activity_form.file.data.save(os.path.join(os.path.abspath(path), UPLOAD_FILE_DIR, filename))
        a_type = ActivityType
        if add_activity_form.activity == ActivityType.Ride.name:
            a_type = ActivityType.Ride
        elif add_activity_form.activity == ActivityType.Run.name:
            a_type = ActivityType.Run
        else:
            a_type = ActivityType.Walk

        activity = PROCESSOR.process_input_data()
        # PROCESSOR.landing_cleanup()
        seconds = (datetime.datetime(2000, 1, 1, 0) + activity[0][1]).time()
        avg_time = activity[0][1] / activity[0][0]
        avg_time = (datetime.datetime(2000, 1, 1, 0) + avg_time).time()
        new_activity = Activity(datetime=activity[0][2], distance=activity[0][0], duration=seconds,
                                average_duration_per_km=avg_time, type=a_type)
        session.save_new_user_activities(current_user.id, new_activity)

    return render_template("personal_dashboard.html", title='Home', form=add_activity_form)


@app.route('/get_personal_stats')
@login_required
def get_personal_stats():
    session = mast.queries.Queries()
    data = session.get_total_distances_by_user_in_last_days(user_id=current_user.id, days=7)
    labels = [key for key, val in data.items()]
    data = [val for key, val in data.items()]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


@app.route('/global_dashboard')
@login_required
def global_dashboard():
    return render_template("global_dashboard.html", title='Global Dashboard')


@app.route('/get_global_contest')
@login_required
def get_global_contest():
    session = mast.queries.Queries()
    labels = ["Where we gonna make it by bike.", "Where we gonna make it on foot."]
    data = [session.get_global_total_distance_on_bike(), session.get_global_total_distance_on_feet()]
    checkpoints = session.get_challenge_parts()
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels, 'checkpoints': checkpoints})})


@app.route('/running_5_km')
@login_required
def running_5_km():
    session = mast.queries.Queries()
    user_five = session.get_best_run_activities_by_user(current_user.id, Competition.Run5km, 10)
    five_runner_men_under = session.get_top_users_best_run(Competition.Run5km, Sex.Male, Age.Under35, 10)
    five_runner_men_above = session.get_top_users_best_run(Competition.Run5km, Sex.Male, Age.Over35, 10)
    five_runner_women_under = session.get_top_users_best_run(Competition.Run5km, Sex.Female, Age.Under35, 10)
    five_runner_women_above = session.get_top_users_best_run(Competition.Run5km, Sex.Female, Age.Over35, 10)

    return render_template("running_5_km.html", title="Running-5", user_five=user_five,
                           five_runner_men_above=five_runner_men_above, five_runner_men_under=five_runner_men_under,
                           five_runner_women_above=five_runner_women_above,
                           five_runner_women_under=five_runner_women_under)


@app.route('/running_10_km')
@login_required
def running_10_km():
    session = mast.queries.Queries()
    user_ten = session.get_best_run_activities_by_user(current_user.id, Competition.Run10km, 10)
    ten_runner_men_under = session.get_top_users_best_run(Competition.Run10km, Sex.Male, Age.Under35, 10)
    ten_runner_men_above = session.get_top_users_best_run(Competition.Run10km, Sex.Male, Age.Over35, 10)
    ten_runner_women_under = session.get_top_users_best_run(Competition.Run10km, Sex.Female, Age.Under35, 10)
    ten_runner_women_above = session.get_top_users_best_run(Competition.Run10km, Sex.Female, Age.Over35, 10)

    return render_template("running_10_km.html", title="Running-10", user_ten=user_ten,
                           ten_runner_men_above=ten_runner_men_above, ten_runner_men_under=ten_runner_men_under,
                           ten_runner_women_above=ten_runner_women_above, ten_runner_women_under=ten_runner_women_under)


@app.route('/running_jogging')
@login_required
def running_jogging():
    session = mast.queries.Queries()
    jogging_global = session.get_top_users_total_distance_on_feet(10)
    jogging_personal = session.get_user_last_activities_on_feet(current_user.id, 10)

    jogging_personal = jogging_personal if jogging_personal else []
    jogging_global = jogging_global if jogging_global else []

    return render_template("running_jogging.html", title="Jogging", jogging_global=jogging_global,
                           jogging_personal=jogging_personal)


@app.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    update_profile_form = UpdateProfileForm(name='up')
    display_update_profile_form = 'none'
    change_password_form = ChangePasswordForm(name='chp')
    display_change_password_form = 'none'
    if request.method == 'POST':
        if request.form['submit'] == 'Update profile':
            update_profile_form = UpdateProfileForm(request.form)
            if update_profile_form.validate():
                current_user.complete_profile(first_name=update_profile_form.first_name.data,
                                              last_name=update_profile_form.last_name.data,
                                              age=update_profile_form.age.data,
                                              sex=update_profile_form.sex.data,
                                              shirt_size=update_profile_form.shirt_size.data,
                                              user_type=update_profile_form.user_type.data,
                                              ukco=update_profile_form.ukco.data,
                                              display_name=update_profile_form.display_name.data,
                                              anonymous=not update_profile_form.competing.data)

                if authenticate_via_sis(name=current_user.first_name, surname=current_user.last_name, login=None,
                                        ukco=current_user.uk_id, is_employee=False):
                    current_user.verify()
            else:
                # Keep the form visible if it contains errors
                display_update_profile_form = 'block'
        elif request.form['submit'] == 'Change password':
            change_password_form = ChangePasswordForm(request.form)
            if change_password_form.validate():
                hashed_password = bcr.generate_password_hash(change_password_form.password.data).decode('UTF-8')
                db.session.query(User).filter(User.id == current_user.id).update({User.password: hashed_password})
                db.session.commit()
                return redirect(url_for('user_settings'))
            else:
                # Keep the form visible if it contains errors
                display_change_password_form = 'block'

    # For GET and after POST method
    return render_template("user_settings.html", title='User Settings',
                           profile=current_user,
                           update_profile_form=update_profile_form,
                           display_update_profile_form=display_update_profile_form,
                           change_password_form=change_password_form,
                           display_change_password_form=display_change_password_form,
                           )


@app.route('/cycling')
@login_required
def cycling():
    session = mast.queries.Queries()
    cyclists_global = session.get_top_users_total_distance_on_bike(10)
    cyclist_personal = session.get_user_last_activities_on_bike(current_user.id, 10)

    cyclist_personal = cyclist_personal if cyclist_personal else []
    cyclists_global = cyclists_global if cyclists_global else []
    return render_template("cycling.html", title="Cycling", cyclist_personal=cyclist_personal,
                           cyclists_global=cyclists_global)


@app.route('/integrations')
@login_required
def integrations():
    return render_template("integrations.html", title='Integrations')
