import json
from flask import request, jsonify, Blueprint, send_from_directory, current_app
from flask_login import current_user, login_required
from mast.tools.json_encoder import MastEncoder
from mast.queries import Queries
import os

views = Blueprint('views', __name__)


@views.route('/get_personal_stats')
@login_required
def get_personal_stats():
    db_query = Queries()
    data = db_query.get_total_distances_by_user_in_last_days(user_id=current_user.id, days=7)
    labels = [str(key) for key, val in data.items()]
    data = [val for key, val in data.items()]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


@views.route('/get_personal_activities')
@login_required
def get_personal_activities():
    db_query = Queries()
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    data = db_query.get_user_last_activities(user_id=current_user.id, number=limit, offset=offset)
    return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)


@views.route('/get_personal_activities_time')
@login_required
def get_personal_activities_time():
    db_query = Queries()
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))

    # TODO: Obsolete, replace by generalized function
    data = db_query.get_best_run_activities_by_user(user_id=current_user.id,
                                                    number=limit, offset=offset)
    enriched_data = []
    order = offset + 1
    for item in data[1]:
        enriched_item = {'order': order,
                         'datetime': item.datetime,
                         'distance': item.distance,
                         'duration': item.duration,
                         'average_duration_per_km': item.average_duration_per_km}
        enriched_data.append(enriched_item)
        order = order + 1
    return json.dumps({'total': data[0], 'rows': enriched_data}, cls=MastEncoder)


@views.route('/get_personal_activities_distance')
@login_required
def get_personal_activities_distance():
    db_query = Queries()
    activity_type = request.args.get('type')
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    if activity_type == 'bike':
        data = db_query.get_user_last_activities_on_bike(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    elif activity_type == 'foot':
        data = db_query.get_user_last_activities_on_foot(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    else:
        return json.dumps({'total': 0, 'rows': []}, cls=MastEncoder)


@views.route('/get_personal_activities_score')
@login_required
def get_personal_activities_score():
    db_query = Queries()
    activity_type = request.args.get('type')
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    if activity_type == 'ride':
        data = db_query.get_user_last_activities_on_bike(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    elif activity_type == 'walk':
        data = db_query.get_user_last_activities_for_walk(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    elif activity_type == 'run':
        data = db_query.get_user_last_activities_for_run(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    elif activity_type == 'inline':
        data = db_query.get_user_last_activities_for_inline(user_id=current_user.id, number=limit, offset=offset)
        return json.dumps({'total': data[0], 'rows': data[1]}, cls=MastEncoder)
    else:
        return json.dumps({'total': 0, 'rows': []}, cls=MastEncoder)


@views.route('/get_best_users_time')
def get_best_users_time():
    db_query = Queries()
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))

    data = db_query.get_top_users_best_run(number=limit, offset=offset)
    enriched_data = []
    order = offset + 1
    for item in data[1]:
        enriched_item = {'order': order,
                         'name': item.User.display(),
                         'datetime': item.Activity.datetime,
                         'duration': item.Activity.duration,
                         'average_duration_per_km': item.Activity.average_duration_per_km}
        enriched_data.append(enriched_item)
        order = order + 1
    return json.dumps({'total': data[0], 'rows': enriched_data}, cls=MastEncoder)


@views.route('/get_best_users_distance')
def get_best_users_distance():
    db_query = Queries()
    activity_type = request.args.get('type')
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))

    if activity_type == 'bike':
        data = db_query.get_top_users_total_distance_on_bike(number=limit, offset=offset)
    elif activity_type == 'foot':
        data = db_query.get_top_users_total_distance_on_foot(number=limit, offset=offset)
    else:
        return json.dumps({'total': 0, 'rows': []}, cls=MastEncoder)

    enriched_data = []
    order = offset + 1
    for item in data[1]:
        enriched_item = {'order': order,
                         'name': item.User.display(),
                         'distance': round(item.total_distance, 1)}
        enriched_data.append(enriched_item)
        order = order + 1
    return json.dumps({'total': data[0], 'rows': enriched_data}, cls=MastEncoder)


@views.route('/get_best_users_score')
def get_best_users_score():
    db_query = Queries()
    activity_type = request.args.get('type')
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))

    if activity_type == 'ride':
        data = db_query.get_top_users_total_score_for_ride(number=limit, offset=offset)
    elif activity_type == 'walk':
        data = db_query.get_top_users_total_score_for_walk(number=limit, offset=offset)
    elif activity_type == 'inline':
        data = db_query.get_top_users_total_score_for_inline(number=limit, offset=offset)
    elif activity_type == 'run':
        data = db_query.get_top_users_total_score_for_run(number=limit, offset=offset)
    else:
        return json.dumps({'total': 0, 'rows': []}, cls=MastEncoder)

    enriched_data = []
    order = offset + 1
    for item in data[1]:
        enriched_item = {'order': order,
                         'name': item.User.display(),
                         'score': int(round(item.total_score, 1))}
        enriched_data.append(enriched_item)
        order = order + 1
    return json.dumps({'total': data[0], 'rows': enriched_data}, cls=MastEncoder)


@views.route('/get_global_contest_combined')
def get_global_contest_combined():
    db_query = Queries()
    label = ["Where we gonna make it by foot or inline."]
    data = [round(db_query.get_global_total_distance_combined(), 1)]
    checkpoints = db_query.get_challenge_parts_to_display()
    return jsonify({'payload': json.dumps({'data': data, 'label': label, 'checkpoints': checkpoints})})


@views.route('/get_global_contest_cyclists')
def get_global_contest_cyclists():
    db_query = Queries()
    label = ["Giro D'Italia."]
    places, data = db_query.get_cyclists_challenge_parts_to_display()
    data = [round(data, 1)]
    altitudes = [x['alt'] for x in places.values()]
    checkpoints = {k: x['target'] for k, x in places.items()}
    return jsonify(
        {'payload': json.dumps({'data': data, 'label': label, 'checkpoints': checkpoints, 'altitudes': altitudes})})


@views.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(current_app.root_path + os.sep + 'static', filename)
