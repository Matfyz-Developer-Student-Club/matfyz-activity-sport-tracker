
import json
import logging
import requests


STRAVA_CLIENT_ID = 61623
STRAVA_CLIENT_SECRET = '71af3bcd89c9a583607db1a383e36f8c1cf6790a' 
REQUESTED_SCOPES = ["activity:read", "read_all"]


def check_strava_permissions(scope):
    given_scopes = scope.split(',')
    for requested in REQUESTED_SCOPES:
        if requested not in given_scopes:
            return False 
    return True

def save_strava_tokens(code):
    url = 'https://www.strava.com/oauth/token'    
    grant_type = 'authorization_code'

    data = {
        'client_id': STRAVA_CLIENT_ID,
	    'client_secret': STRAVA_CLIENT_SECRET,
	    'code': code,
	    'grant_type': grant_type
    }
    
    response = requests.post(url, data=data)

    response_data = json.loads(response.text)
    #logging.info(json.dumps(response_data, indent=4)) # this is JSON containing access and refresh token as well as athlete info

    #TODO: save into database
    #current_user.strava_id = response_data["athlete"]["id"]
    #current_user.strava_refresh_token = response_data["refresh_token"]
    #current_user.strava_access_token = response_data["access_token"]

    #TODO: DELETE
    get_activities(response_data["access_token"])

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
