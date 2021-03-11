import json
import requests
from flask_login import current_user
from datetime import time
from mast.queries import Queries

# TODO: remove
import logging
strava_logger = logging.getLogger('STRAVA')

# TODO: change these in the production since they are already public
STRAVA_CLIENT_ID = 61623
STRAVA_CLIENT_SECRET = '71af3bcd89c9a583607db1a383e36f8c1cf6790a' 
STRAVA_SCOPE = ['activity:read']


class ExpiredAccessToken(Exception) :
    pass


def check_strava_permissions(scope):
    given_scopes = scope.split(',')
    for requested in STRAVA_SCOPE:
        if requested not in given_scopes:
            return False 
    return True


def save_strava_tokens(auth_code):
    url = 'https://www.strava.com/oauth/token'    
    data = {
        'client_id': STRAVA_CLIENT_ID,
	    'client_secret': STRAVA_CLIENT_SECRET,
	    'code': auth_code,
	    'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=data)
    response_data = json.loads(response.text)

    strava_logger.info(json.dumps(response_data, indent=4)) # this is JSON containing access and refresh token as well as athlete info
    '''
    INFO:root:{
        "token_type": "Bearer",
        "expires_at": 1615131642,
        "expires_in": 21363,
        "refresh_token": "226b0fc8f844e4e8ebef13ca5aee36d21039746c",
        "access_token": "f889f917b27823a54ce7b6186e7c397e02b5247e",
        "athlete": {
            "id": 77482880,
            "username": "drozdkt",
            "resource_state": 2,
            "firstname": "Tom\u00e1\u0161",
            "lastname": "Drozd\u00edk",
            "bio": null,
            "city": null,
            "state": null,
            "country": null,
            "sex": "M",
            "premium": false,
            "summit": false,
            "created_at": "2021-01-31T17:33:25Z",
            "updated_at": "2021-02-08T17:05:17Z",
            "badge_type_id": 0,
            "weight": 0.0,
            "profile_medium": "https://lh3.googleusercontent.com/-aW_D6lEIPks/AAAAAAAAAAI/AAAAAAAAAAA/AMZuuckvXZa5BpjtkjbodCd6tkLjqrcuQA/s96-c/photo.jpg",
            "profile": "https://lh3.googleusercontent.com/-aW_D6lEIPks/AAAAAAAAAAI/AAAAAAAAAAA/AMZuuckvXZa5BpjtkjbodCd6tkLjqrcuQA/s96-c/photo.jpg",
            "friend": null,
            "follower": null
        }
    }
    '''

    current_user.strava_id = response_data["athlete"]["id"]
    current_user.strava_refresh_token = response_data["refresh_token"]
    current_user.strava_access_token = response_data["access_token"]


def refresh_access_token():
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
        'client_id': STRAVA_CLIENT_ID,
	    'client_secret': STRAVA_CLIENT_SECRET,
	    'grant_type': 'refresh_token',
	    'refresh_token': current_user.strava_refresh_token
    }
    response = requests.post(url, data=data)
    response_data = json.loads(response.text)

    strava_logger.info(json.dumps(response_data, indent=4))

    # We have to renew both refresh and access token
    current_user.strava_access_token = response_data['access_token']
    current_user.strava_refresh_token = response_data['refresh_token']
    current_user.strava_expires_at = int(response_data['expires_at'])


def get_athlete(access_token):
    '''
    Request:
    $ http GET "https://www.strava.com/api/v3/athlete" "Authorization: Bearer [[token]]"
    
    Return:
        some JSON

    Errors:
        may need refresh
    '''
    url="https://www.strava.com/api/v3/athlete"
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.request('GET', url, headers=header)
    json_data = json.loads(response.text)
    strava_logger.info(json.dumps(json_data, indent=4))


def get_activity(access_token, activity_id):
    url = f'https://www.strava.com/api/v3/activities/{activity_id}'
    header = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'include_all_efforts': False
    }

    response = requests.request('GET', url, headers=header, data=data)
    json_data = json.loads(response.text)
    #strava_logger.info(json.dumps(json_data, indent=4))

    return json_data


def get_athlete_activities(access_token, after:int=1614556800, before:int = None, per_page:int = 100, page:int = 1):
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
    #strava_logger.info(json.dumps(json_data, indent=4))

    return json_data


def get_activity_info(activity:json):
    '''
    Parses json of STRAVA SummaryActivity.
    :param activity: json of an activity
    :return: (name:str, distance:float, total_time:time, elevation:float, pace:time, strava_type:str)
    '''
    distance = activity['distance']
    time_in_secs = activity['moving_time']
    total_time = get_time(time_in_secs)
    elevation = activity['total_elevation_gain'] if not None else 0
    strava_type = activity['type']  # https://developers.strava.com/docs/reference/#api-models-ActivityType
    name = activity['name'][:30] if not None else ''
    pace = get_time(round(time_in_secs / distance * 1000))

    return (name, distance, total_time, elevation, pace, strava_type)


def get_activity_from_webhook(data:json):
    if data['aspect_type'] != 'create':
        return None
    db_query = Queries(credit=True)
    db_res = db_query.get_user_access_token(data['owner_id'])
    if (db_res[0] != 1):
        return None
    access_token = db_res[1][0] # get first access_token form list at index 1
    activity_id = data['object_id']

    return get_activity(access_token, activity_id)

def get_time(in_time):
    '''
    Gets time from seconds
    :param in_time: time in seconds
    :return: datetime.time instance
    '''
    hours = (in_time) // 3600     # 3600 secs in hour
    minutes = ((in_time) % 3600) // 60    # take off hours and 60 sec in minute
    seconds = ((in_time) % 3600) % 60     # take off hours, take off
    return time(hours, minutes, seconds)
