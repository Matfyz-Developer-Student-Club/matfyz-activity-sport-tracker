import json
from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required
from mast.tools.json_encoder import MastEncoder
from mast.queries import Queries

views = Blueprint('views', __name__)


@views.route('/get_personal_stats')
@login_required
def get_personal_stats():
    db_query = Queries(credit=True)
    data = db_query.get_total_distances_by_user_in_last_days(user_id=current_user.id, days=7)
    labels = [key for key, val in data.items()]
    data = [val for key, val in data.items()]
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels})})


@views.route('/get_personal_activities')
@login_required
def get_personal_activities():
    db_query = Queries(credit=True)
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


@views.route('/get_global_contest')
def get_global_contest():
    db_query = Queries()
    labels = ["Where we gonna make it by bike.",
              "Where we gonna make it on foot."]
    data = [round(db_query.get_global_total_distance_on_bike(), 1),
            round(db_query.get_global_total_distance_on_foot(), 1)]
    checkpoints = db_query.get_challenge_parts_to_display()
    return jsonify({'payload': json.dumps({'data': data, 'labels': labels, 'checkpoints': checkpoints})})
