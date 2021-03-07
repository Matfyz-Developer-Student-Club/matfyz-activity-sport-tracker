import mast
import requests
from flask import redirect, request, render_template, url_for, Blueprint, flash
from flask_login import current_user, login_required
from mast.session import Session
from mast.integrations.strava import *
from mast.session import Session

integrations = Blueprint('integrations', __name__)

# TODO: investigate why https does not work
BASE_URL = 'http://localhost:5000'


@integrations.route('/strava/init', methods=['GET'])
@login_required
def strava_init():
    scope = ','.join(STRAVA_SCOPE)
    redirect_uri = BASE_URL + url_for('integrations.strava_auth')
    return redirect(f"http://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope={scope}")


@integrations.route('/strava/auth', methods=['GET'])
def strava_auth():
    '''
    request = "GET /strava/auth?state=&code=2db1b5fbcc4aae3815caf2988a4ae871592912d8&scope=read,read_all HTTP/1.1"
    inspect request code and scope
    if scope is not valid then display error msg
    '''
    auth_code = request.args.get('code')
    scope = request.args.get('scope')

    if not check_strava_permissions(scope):
        flash('You have not provided all required permissions. Try again and agree with all permissions.', 'danger')
        return render_template("integrations.html", title='Integrations')

    save_strava_tokens(auth_code)
    return render_template("integrations.html", title='Integrations')


@integrations.route('/strava/webhook', methods=['POST'])
def strava_webhook():
    """
        https://developers.strava.com/docs/webhooks
    """
    pass