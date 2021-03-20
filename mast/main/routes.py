import os
import datetime
from flask import redirect, request, render_template, url_for, Blueprint, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from mast.main.forms import CreditsForm, AddActivityForm
from mast.models import UserType, Activity, ActivityType
from mast.tools.utils import check_profile_verified
from mast.session import Session
from mast.queries import Queries

main = Blueprint('main', __name__)


@main.route('/faq')
@login_required
def faq():
    session_data = Session()
    check_profile_verified(session_data)
    return render_template("faq.html", title='Frequently Asked Questions', session_data=session_data)


@main.route('/about_competitions')
@login_required
def about_competitions():
    session_data = Session()
    check_profile_verified(session_data)
    return render_template("about_competitions.html", title='About Competitions', session_data=session_data)


@main.route('/integrations')
@login_required
def integrations():
    db_query = Queries()
    session_data = Session()
    check_profile_verified(session_data)
    favorite_activities = db_query.get_user_favorite_activity(current_user.id)
    return render_template("integrations.html", title='Integrations', session_data=session_data,
                           favorite_activities=favorite_activities)


@main.route("/statistics")
def statistics():
    db_query = Queries()
    stats = db_query.get_stats()
    return render_template("statistics.html", title='Statistics', stats=stats)


@main.route("/credits", methods=['GET', 'POST'])
def display_credits():
    if request.method == 'GET':
        form = CreditsForm('credits_form')
        return render_template('credits.html', title='Credits', authorized=False, form=form)
    else:
        form = CreditsForm(request.form)
        if form.validate_on_submit():
            if form.password.data == 'KTV2020':  # TODO: Obsoleted
                db_query = Queries(credit=True)
                students = db_query.get_students()
                return render_template('credits.html', title='Credits', authorized=True, students=students)
            else:
                form.password.errors.append('Specified password is invalid!')
                return render_template('credits.html', title='Credits', authorized=False, form=form)
        else:
            return render_template('credits.html', title='Credits', authorized=False, form=form)


@main.route('/personal_dashboard', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    session_data = Session()
    db_query = Queries(credit=True)
    add_activity_form = AddActivityForm()
    if add_activity_form.validate_on_submit():
        filename = secure_filename(add_activity_form.file.data.filename)
        path = os.path.join(__file__, os.pardir)
        add_activity_form.file.data.save(os.path.join(
            os.path.abspath(path), current_app.config['UPLOAD_FILE_DIR'], filename))

        if add_activity_form.activity.data == ActivityType.Ride.name:
            a_type = ActivityType.Ride
        elif add_activity_form.activity.data == ActivityType.Run.name:
            a_type = ActivityType.Run
        else:
            a_type = ActivityType.Walk

        activity = current_app.config['PROCESSOR'].process_input_data(filename)
        current_app.config['PROCESSOR'].landing_cleanup(filename)
        distance = activity[0]
        seconds = activity[1].total_seconds()
        start_time = activity[2]

        if distance == 0:
            session_data.warning('Activity of zero distance ignored.')
        elif start_time is None:
            if a_type == ActivityType.Run:
                a_type = ActivityType.Walk
            start_time = datetime.datetime.now().replace(microsecond=0)
            full_time = datetime.time()
            avg_time = datetime.time()
            new_activity = Activity(datetime=start_time, distance=distance, duration=full_time,
                                    average_duration_per_km=avg_time, type=a_type)
            db_query.save_new_user_activities(current_user.id, new_activity)
            session_data.info(str(a_type) + ' activity of ' + str(distance) + ' km added.')
        else:
            avg_seconds = round(seconds / distance)
            full_time = (datetime.datetime(2000, 1, 1, 0) + datetime.timedelta(seconds=seconds)).time()
            avg_time = (datetime.datetime(2000, 1, 1, 0) + datetime.timedelta(seconds=avg_seconds)).time()
            new_activity = Activity(datetime=start_time, distance=distance, duration=full_time,
                                    average_duration_per_km=avg_time, type=a_type)
            db_query.save_new_user_activities(current_user.id, new_activity)
            session_data.info(str(a_type) + ' activity of ' + str(distance) + ' km added.')

        return redirect(url_for('main.home'))

    check_profile_verified(session_data)
    total_foot = db_query.get_total_distance_by_user_on_foot(current_user.id) or 0
    total_bike = db_query.get_total_distance_by_user_on_bike(current_user.id) or 0
    total_credit = None
    if current_user.type == UserType.Student:
        total_credit = round(total_foot + total_bike / 2, 2)

    return render_template("personal_dashboard.html", title='Home', form=add_activity_form,
                           total_foot=total_foot, total_bike=total_bike, total_credit=total_credit,
                           season=db_query.SEASON_COMPETITION, season_credit=db_query.SEASON_CREDIT,
                           session_data=session_data)
