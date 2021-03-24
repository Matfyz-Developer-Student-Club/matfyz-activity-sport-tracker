import json
import logging
import requests
from flask import current_app, flash
from flask_login import current_user
from datetime import time, datetime
from time import time as t
from mast.queries import Queries
from mast.models import Activity, ActivityType, Sex, User
from mast.tools.points import Points
from mast import db
from math import floor

strava_logger = logging.getLogger('STRAVA')


def check_strava_permissions(scope):
    given_scopes = scope.split(',')
    for requested in current_app.config['STRAVA_SCOPE']:
        if requested not in given_scopes:
            return False
    return True


def check_strava_id_is_used(strava_id: int) -> bool:
    db_queries = Queries()
    athletes = db_queries.get_user_by_strava_id(strava_id)
    if len(athletes) > 0:
        return True
    return False


def save_strava_tokens(auth_code):
    ''' Acquire authentication and refresh token as well as info about an athlete with an authentication code.
    '''

    url = 'https://www.strava.com/oauth/token'
    data = {
        'client_id': current_app.config['STRAVA_CLIENT_ID'],
        'client_secret': current_app.config['STRAVA_CLIENT_SECRET'],
        'code': auth_code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=data)
    response_data = json.loads(response.text)

    # This is JSON containing access and refresh token as well as athlete info
    strava_logger.info( json.dumps(response_data, indent=4))

    if check_strava_id_is_used(response_data["athlete"]["id"]):
        flash('This STRAVA account is already used by another user.', 'danger')

    current_user.strava_id = response_data["athlete"]["id"]
    current_user.strava_refresh_token = response_data["refresh_token"]
    current_user.strava_access_token = response_data["access_token"]
    current_user.strava_expires_at = int(response_data["expires_at"])
    db.session.add(current_user)
    db.session.commit()

def refresh_access_token(user:User):
    '''
    Request:
    curl -X POST https://www.strava.com/api/v3/oauth/token \
        -d client_id=ReplaceWithClientID \
        -d client_secret=ReplaceWithClientSecret \
        -d grant_type=refresh_token \
        -d refresh_token=ReplaceWithRefreshToken

    Return:
    {
        "token_type": "Bearer",
        "access_token": "a9b723...",
        "expires_at":1568775134,
        "expires_in":20566,
        "refresh_token":"b5c569..."
    }
    '''
    url = 'https://www.strava.com/api/v3/oauth/token'
    data = {
        'client_id': current_app.config['STRAVA_CLIENT_ID'],
        'client_secret': current_app.config['STRAVA_CLIENT_SECRET'],
        'grant_type': 'refresh_token',
        'refresh_token': user.strava_refresh_token
    }
    response = requests.post(url, data=data)
    response_data = json.loads(response.text)

    strava_logger.info(json.dumps(response_data, indent=4))

    # We have to renew both refresh and access token
    user.strava_access_token = response_data['access_token']
    user.strava_refresh_token = response_data['refresh_token']
    user.strava_expires_at = int(response_data['expires_at'])

def get_athlete(access_token):
    '''
    Request:
    $ http GET "https://www.strava.com/api/v3/athlete" "Authorization: Bearer [[token]]"

    Return:
        some JSON

    Errors:
        may need refresh
    '''
    url = "https://www.strava.com/api/v3/athlete"
    header = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.request('GET', url, headers=header)
    json_data = json.loads(response.text)
    strava_logger.info(json.dumps(json_data, indent=4))


def get_activity(access_token, strava_activity_id):
    url = f'https://www.strava.com/api/v3/activities/{strava_activity_id}'
    header = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'include_all_efforts': False
    }

    response = requests.request('GET', url, headers=header, data=data)
    json_data = json.loads(response.text)
    # strava_logger.info(json.dumps(json_data, indent=4))

    return json_data


def get_athlete_activities(access_token, after: int = 1614556800, before: int = None, per_page: int = 100,
                           page: int = 1):
    '''
    Returns list of user activities after 3.1.2021
    :param access_token: acces token of currentuser
    :param after: UNIX epoch timestamp - will list activities after given time - default 3.1.2021 00:00
    :param before: UNIX epoch timestamp - will list activities before given time
    :param per_page: activities per page - default 100
    :param page: pages - default 1
    :return: JSON of list of activities
    '''
    url = f'https://www.strava.com/api/v3/athlete/activities'

    header = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'before': before if not None else '',
        'after': after,
        'page': page,
        'per_page': per_page
    }

    response = requests.request('GET', url, headers=header, data=data)
    json_data = json.loads(response.text)
    # strava_logger.info(json.dumps(json_data, indent=4))

    return json_data


def create_activity_from_strava_json(activity: dict, user: User, strava_activity_id: int) -> Activity:
    """
    Processes json from strava *DetailedActivity* and creates Activity instance
    :param activity: json from strava *strava.com/activity/id*
    :param user: User that uploaded the activity
    :param strava_activity_id: strava activity id
    :return: new Activity ready to save into database
    """

    distance = activity['distance']     # meters
    time_in_secs = activity['moving_time']  # seconds
    total_time = _get_time(time_in_secs)     # time(H:M:S)
    elevation = activity['total_elevation_gain'] if not None else 0     # meters
    activity_type = _get_activity_type(activity['type'])  # https://developers.strava.com/docs/reference/#api-models-ActivityType
    name = activity['name'][:30] if not None else ''    # string
    pace = _get_time(round(time_in_secs / distance * 1000))     # minutes per km
    activity_date = datetime.strptime(activity['start_date'],'%Y-%m-%dT%H:%M:%SZ')  # datetime
    score = _get_score(distance / 1000, elevation, pace, user, activity_type)     # int

    # check activity constrains
    if activity_type is None:    # unsupported ActivityType
        strava_logger.info(
            f'Activity :{activity_type} is not supported.')
        return None

    if _satisfy_distance_constrains(distance/1000, activity_type):     # Activity is not long enough to be counted
        strava_logger.info(
            f'Activity :{activity_type} of length {distance} meters does not satisfy distance constrains.')
        return None

    # creation of the activity
    new_activity = Activity()
    new_activity.datetime = activity_date
    new_activity.distance = distance / 1000
    new_activity.duration = total_time
    new_activity.average_duration_per_km = pace
    new_activity.type = activity_type
    new_activity.user_id = user.id
    new_activity.name = name
    new_activity.elevation = elevation
    new_activity.strava_id = strava_activity_id
    new_activity.score = score

    return new_activity


def process_strava_webhook(data: dict):
    """
    Processes strava webhook
    :param data: dictionary of data from webhook
    :return: On Create: Activity; On Delete: None; On Update: None
    """
    user = _get_user(data)
    if user is None:
        strava_logger.info(
            f'User with strava_id:{data["owner_id"]} was not found, but create webhook was recieved')
        strava_logger.info(data)
        return

    # Check whether the access token for given user already expired with some reserve, if it did then refresh tokens
    if user.strava_expires_at - current_app.config['STRAVA_EXPIRE_RESERVE'] > floor(t()):
        refresh_access_token(user)

    # Process incomming webhook based on object type
    if data['object_type'] == 'athlete':
        strava_logger.info('Webhook sent info about athlete')
        return

    # Process incomming webhook based on aspect type
    try:
        if data['aspect_type'] == 'create':
            strava_logger.info('Webhook sent info about activity creation')
            _store_activity(user, data)
            return

        elif data['aspect_type'] == 'delete':
            strava_logger.info('Webhook sent info about activity delete')
            _delete_activity(data)
            return

        elif data['aspect_type'] == 'update':
            strava_logger.info('Webhook sent info about activity update')
            _update_activity(data)
            return

        else:
            strava_logger.info(f'Webhook with unknown aspect_type: recieved: ')
            strava_logger.info(data)
            return
    except Exception as e:
        strava_logger.error(f'Processing webhook {data} returned an exception: {e}')


def _store_activity(user, data):
    strava_activity_id = data['object_id']
    activity_data = get_activity(user.strava_access_token, strava_activity_id)
    activity = create_activity_from_strava_json(activity_data, user, strava_activity_id)

    db_query = Queries()

    #do not allow same activity to be uploaded twice
    existing_activities = db_query.get_activity_by_strava_id(strava_activity_id)
    if len(existing_activities) > 0:
        return

    db_query.save_new_user_activities(activity.user_id, activity)


def _delete_activity(data):
    strava_activity_id = data['object_id']
    db_query = Queries()
    db_query.delete_activity_by_strava_id(strava_activity_id)


def _update_activity(data):
    strava_activity_id = data['object_id']

    # parse data to update
    new_title = data['updates']['title'] if 'title' in data['updates'].keys() else None
    new_type = data['updates']['type'] if 'type' in data['updates'].keys() else None
    is_private = data['updates']['private'] if 'private' in data['updates'].keys() else False

    # changed to private -> delete activity
    if is_private:
        db_query = Queries()
        db_query.delete_activity_by_strava_id(strava_activity_id)
        return

    # create dict for update query
    data_to_update = dict()
    if new_title:
        data_to_update['name'] = new_title
    if new_type:
        data_to_update['type'] = _get_activity_type(new_type)

    # update database
    db_query = Queries()
    db_query.update_activity_info(strava_activity_id, data_to_update)


def _get_user(data):
    db_query = Queries()
    db_res = db_query.get_user_by_strava_id(data['owner_id'])
    if len(db_res) != 1:
        return None
    return db_res[0]


def _get_activity_type(strava_activity:str) -> ActivityType:
    for a in ActivityType:
        if str(a) == strava_activity:
            return a
    return None


def _get_time(in_time):
    '''
    Gets time from seconds
    :param in_time: time in seconds
    :return: datetime.time instance
    '''
    hours = in_time // 3600  # 3600 secs in hour
    minutes = (in_time % 3600) // 60  # take off hours and 60 sec in minute
    seconds = (in_time % 3600) % 60  # take off hours, take off
    return time(hours, minutes, seconds)


def _satisfy_distance_constrains(distance:int , type:ActivityType) -> bool:
    """

    :param distance: distance in METERS
    :param type: type of Activity
    :return: True if distance constrains are satisfied, False otherwise
    """
    # TODO: UPDATE when new activity is introduced
    LIMITS = {
        ActivityType.Run: 3000,
        ActivityType.Walk: 5000,
        ActivityType.InlineSkate: 8000,
        ActivityType.Ride: 10000
    }

    return True if distance >= LIMITS[type] else False


def _get_score(distance:float, elevation:float, pace:time, user:User, activity_type:ActivityType) -> int:
    """

    :param distance: distance in KM
    :param elevation: elevation in M
    :param pace: pace in minutes on KM
    :param user: User who uploaded the activity
    :param activity_type: ActivityType
    :return: integer of score
    """
    point = Points()
    
    # UPDATE when new activity is introduced
    function_mapping = {
        ActivityType.Run: point.get_run_activity_points,
        ActivityType.Walk: point.get_walk_activity_points,
        ActivityType.Ride: point.get_ride_activity_points,
        ActivityType.InlineSkate: point.get_inline_activity_points,
    }
    return function_mapping[activity_type](user, elevation, distance, pace)
