import json
import requests
from flask_login import current_user

# TODO: remove
import logging

# TODO: change these in the production since they are already public
STRAVA_CLIENT_ID = 61623
STRAVA_CLIENT_SECRET = '71af3bcd89c9a583607db1a383e36f8c1cf6790a' 
STRAVA_SCOPE = ["activity:read", "read_all"]

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

    logging.info(json.dumps(response_data, indent=4)) # this is JSON containing access and refresh token as well as athlete info
    """
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
    """

    current_user.strava_id = response_data["athlete"]["id"]
    current_user.strava_refresh_token = response_data["refresh_token"]
    current_user.strava_access_token = response_data["access_token"]


def renew_access_token():
    pass


def get_athlete(access_token):
    '''
    $ http GET "https://www.strava.com/api/v3/athlete" "Authorization: Bearer [[token]]"
    
    Returns:
        some JSON
    '''
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    url="https://www.strava.com/api/v3/athlete"
    
    response = requests.request('GET', url, headers=header)
    json_data = json.loads(response.text)
    logging.info(json.dumps(json_data, indent=4))


def get_activities(access_token):
    '''
    $ http GET "https://www.strava.com/api/v3/athlete/activities?before=&after=&page=&per_page=" "Authorization: Bearer [[token]]"

    Returns:
        some JSON
    '''
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    url="https://www.strava.com/api/v3/athlete/activities"
    
    response = requests.request('GET', url, headers=header)
    json_data = json.loads(response.text)
    logging.info(json.dumps(json_data, indent=4))
