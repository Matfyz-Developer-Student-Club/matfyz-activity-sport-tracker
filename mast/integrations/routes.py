import mast
import requests
from flask import redirect, request, url_for, Blueprint
from flask_login import login_required
from mast.session import Session
from mast.integrations import *

integrations = Blueprint('integrations', __name__)

# TODO: change these in the production since they are already public
STRAVA_CLIENT_ID = 61623
STRAVA_CLIENT_SECRET = '71af3bcd89c9a583607db1a383e36f8c1cf6790a' 
BASE_URL = 'http://localhost:5000' # TODO: investigate why https does not work

@integrations.route('/strava/init', methods=['GET', 'POST'])
@login_required
def strava_init():
    scope = "read_all,activity:read"
    redirect_uri = BASE_URL + url_for('integrations.strava_auth')
    return redirect(f"http://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope={scope}")

@integrations.route('/strava/auth', methods=['GET'])
@login_required
def strava_auth():
    # request = "GET /strava/auth?state=&code=2db1b5fbcc4aae3815caf2988a4ae871592912d8&scope=read,read_all HTTP/1.1"
    # TODO: inspect request code and scope
    # if scope is not valid then display error msg
    code = request.args.get('code')
    scope = request.args.get('scope')

    if not check_strava_permissions(scope):
        #TODO: tell user to fuck off
        # return to page that tells user to fuck off
        return "nonono"

    logging.info("CODE: " + code)
    logging.info("SCOPE: " + scope)
    save_strava_tokens(code)
    #get_activities()
    return 'hello'
