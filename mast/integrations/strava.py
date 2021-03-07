import json
import requests
from flask_login import current_user

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
    '''
    $ http GET "https://www.strava.com/api/v3/activities/{id}?include_all_efforts=" "Authorization: Bearer [[token]]"

    Returns:
        some JSON
    '''
    url='https://www.strava.com/api/v3/athlete/activities'
    header = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'include_all_efforts': False
    }
    
    response = requests.request('GET', url, headers=header, data=data)
    json_data = json.loads(response.text)
    strava_logger.info(json.dumps(json_data, indent=4))

