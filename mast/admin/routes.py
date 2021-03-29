from flask import Response, redirect, request, render_template, url_for, Blueprint, flash, jsonify
from flask_login import current_user, login_required
from flask import current_app
from mast.integrations.utils import check_strava_permissions, save_strava_tokens, process_strava_webhook, \
    add_activities_in_competition_season
from mast.session import Session
from mast.queries import Queries
import logging
from mast.admin.utils import send_suspicious_activity_email
from mast.tools.points import Points
from mast.integrations.utils import get_score
from mast import db

admin = Blueprint('admin', __name__)


@admin.route("/admin/panel", methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.role.is_admin():
        db_queries = Queries()
        return render_template("admin_panel.html", users=db_queries.enumerate_admin_stats())
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
        logger.info(f"Processing user: {user.first_name} {user.last_name}")
        add_activities_in_competition_season(user)

    flash("Activities updated.", category="info")

    return jsonify({"body": "Activities were updated.", "ok": True, "redirect": url_for('admin.admin_panel')})
