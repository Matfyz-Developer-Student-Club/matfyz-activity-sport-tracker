from flask import Response, redirect, request, render_template, url_for, Blueprint, flash, jsonify
from flask_login import current_user, login_required
from flask import current_app
from mast.integrations.utils import check_strava_permissions, save_strava_tokens, process_strava_webhook, \
    add_activities_in_competition_season, refresh_access_token
from mast.models import ActivityType
from mast.session import Session
from mast.queries import Queries
import logging
from mast.admin.utils import send_suspicious_activity_email, get_statistics
from mast.tools.points import Points
from mast.integrations.utils import get_score
from mast import db

admin = Blueprint('admin', __name__)


@admin.route("/admin/panel", methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.role.is_admin():
        db_queries = Queries()
        users = db_queries.enumerate_admin_stats()
        competing_users = len([user for user in users if user.strava_id])
        return render_template("admin_panel.html", users=users, competing_users=competing_users)
    else:
        flash(f"User {current_user.first_name} {current_user.last_name} does not have permission to see this page",
              "danger")
        return redirect(url_for('main.home'))


@admin.route("/admin/suspicious_activity", methods=['GET', 'POST'])
@login_required
def suspicious_activity_endpoint():
    db_query = Queries()
    activity_id = int(request.args.get("activity_id"))
    activity = db_query.get_activity_by_id(activity_id)
    user = db_query.get_user_by_id(activity.user_id)
    send_suspicious_activity_email(activity, user)
    flash("User was notified.", category="info")

    return jsonify({"body": "User was notified.", "ok": True, "redirect": url_for('admin.admin_panel')})


@admin.route('/admin/reevaluate_all_score')
@login_required
def re_evaluate_all_users_score():
    if current_user.role.is_admin():
        db_query = Queries()
        users = db_query.enumerate_admin_stats()

        for user in users:
            for activity in user.activities:
                score = get_score(activity.distance, activity.elevation, activity.average_duration_per_km, user,
                                  activity.type)
                activity.score = score
                db.session.add(activity)

        db.session.commit()
        flash("Activity score was successfully re-evaluated", 'success')

        return jsonify({"ok": True, "redirect": url_for('admin.admin_panel')})

    return jsonify({"ok": False, "redirect": url_for('admin.admin_panel')})


@admin.route("/admin/fetch_season_activities", methods=['GET', 'POST'])
@login_required
def get_all_activities_in_season():
    db_query = Queries()
    users = db_query.get_all_users()
    logger = logging.getLogger('STRAVA')
    for user in users:
        if user.strava_id:
            logger.info(f"Processing user: {user.first_name} {user.last_name} {user.email}")
            refresh_access_token(user)
            add_activities_in_competition_season(user)
        else:
            logger.info(f"Skipping user: {user.first_name} {user.last_name} {user.email}")
            continue

    flash("Activities updated.", category="info")

    return jsonify({"body": "Activities were updated.", "ok": True, "redirect": url_for('admin.admin_panel')})


@admin.route("/admin/fetch_user_season_activities", methods=['GET'])
@login_required
def get_user_activities_in_season():
    db_query = Queries()
    user_id = int(request.args.get("user_id"))
    user = db_query.get_user_by_id(user_id)
    logger = logging.getLogger('STRAVA')
    if user.strava_id is None:
        logger.info(f"User {user.first_name} {user.last_name}, email {user.email} is not authenticated via STRAVA")
        return jsonify({"ok": False, "redirect": url_for('admin.admin_panel')})

    refresh_access_token(user)
    add_activities_in_competition_season(user)

    flash("User activities of current season fetched.", category="info")
    return jsonify({"body": "Activities fetched.", "ok": True, "redirect": url_for('admin.admin_panel')})


@admin.route('/admin/delete_non_season_activities')
@login_required
def delete_non_season_activities():
    if current_user.role.is_admin():
        db_query = Queries()
        activities = db_query.get_all_activities()
        logger = logging.getLogger('STRAVA')
        for activity in activities:
            if not activity.satisfies_constraints():
                logger.info(f"Deleting activity of type: {activity.type} of length {activity.distance}")
                db_query.delete_activity_by_strava_id(activity.strava_id)

        db.session.commit()
        flash("Activities were successfully deleted", 'success')

        return jsonify({"ok": True, "redirect": url_for('admin.admin_panel')})

    return jsonify({"ok": False, "redirect": url_for('admin.admin_panel')})


@admin.route("/admin/statistics", methods=['GET', 'POST'])
@login_required
def admin_statistics():
    if current_user.role.is_admin():
        data = list()
        data.append(get_statistics(ActivityType.Run))
        data.append(get_statistics(ActivityType.Walk))
        data.append(get_statistics(ActivityType.Ride))
        data.append(get_statistics(ActivityType.InlineSkate))

        return render_template("admin_statistics.html", data=data)
    else:
        flash(f"User {current_user.first_name} {current_user.last_name} does not have permission to see this page",
              "danger")
        return redirect(url_for('main.home'))
