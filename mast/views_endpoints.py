import json
import mast
from flask import request, jsonify
from flask_login import current_user, login_required
from mast.models import User, Competition, Sex, Age, Activity, ActivityType
from mast.json_encoder import MastEncoder
from mast import queries, app


@app.route('/get_personal_stats')
@login_required
def get_personal_stats():
    db_query = mast.queries.Queries()
    data = db_query.get_total_distances_by_user_in_last_days(user_id=current_user.id, days=7)
    labels = [key for key, val in data.items()]
    data = [val for key, val in data.items()]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


@app.route('/get_personal_activities')
@login_required
def get_personal_activities():
    db_query = mast.queries.Queries()
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    data = db_query.get_user_last_activities(user_id=current_user.id, number=limit, offset=offset)
    return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)


@app.route('/get_personal_activities_time')
@login_required
def get_personal_activities_time():
    db_query = mast.queries.Queries()
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    data = db_query.get_user_last_activities(user_id=current_user.id, number=limit, offset=offset)
    return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)


@app.route('/get_personal_activities_distance')
@login_required
def get_personal_activities_distance():
    db_query = mast.queries.Queries()
    activity_type = request.args.get('type')
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    if activity_type == 'bike':
        data = db_query.get_user_last_activities_on_bike(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    elif activity_type == 'foot':
        data = db_query.get_user_last_activities_on_foot(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    else:
        return json.dumps({'total': 0, 'rows': []}, cls=MastEncoder)


@app.route('/get_global_contest')
@login_required
def get_global_contest():
    db_query = mast.queries.Queries()
    labels = ["Where we gonna make it by bike.",
              "Where we gonna make it on foot."]
    data = [round(db_query.get_global_total_distance_on_bike(), 1),
            round(db_query.get_global_total_distance_on_foot(), 1)]
    checkpoints = db_query.get_challenge_parts_to_display()
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels, 'checkpoints': checkpoints})})
