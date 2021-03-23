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
def faq():
    if current_user.is_authenticated:
        session_data = Session()
        check_profile_verified(session_data)
        return render_template("faq.html", title="Frequently Asked Questions", session_data=session_data)
    else:
        return render_template("faq_public.html", title="Frequently Asked Questions")


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
                db_query = Queries()
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
    db_query = Queries()

    check_profile_verified(session_data)
    total_run_score = db_query.get_total_score_by_user_for_run(current_user.id) or 0
    total_walk_score = db_query.get_total_score_by_user_for_walk(current_user.id) or 0
    total_inline_score = db_query.get_total_score_by_user_for_inline(current_user.id) or 0
    total_ride_score = db_query.get_total_score_by_user_for_ride(current_user.id) or 0

    return render_template("personal_dashboard.html", title='Home',
                           total_run_score=total_run_score, total_walk_score=total_walk_score,
                           total_inline_score=total_inline_score, total_ride_score=total_ride_score,
                           season=db_query.SEASON_COMPETITION, session_data=session_data)
