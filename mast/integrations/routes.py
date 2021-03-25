from flask import Response, redirect, request, render_template, url_for, Blueprint, flash, jsonify
from flask_login import current_user, login_required
from flask import current_app
from mast.integrations.utils import check_strava_permissions, save_strava_tokens, process_strava_webhook
from mast.session import Session
import logging
from mast import csrf

integrations = Blueprint('integrations', __name__)

# TODO: replace with http:// + SERVER_NAME on test server, on local debug replace with localhost
#       though this will work only for strava authentication not on webhooks
BASE_URL = 'http://mathletics-test.ks.matfyz.cz'


@integrations.route('/strava/init', methods=['GET'])
@login_required
def strava_init():
    scope = ','.join(current_app.config['STRAVA_SCOPE'])
    redirect_uri = BASE_URL + url_for('integrations.strava_auth')
    logging.info(f"******** REDIRECT URI {redirect_uri} *******")
    return redirect(f"http://www.strava.com/oauth/authorize?client_id={current_app.config['STRAVA_CLIENT_ID']}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope={scope}")


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
        return redirect(url_for('main.integrations'))

    save_strava_tokens(auth_code)
    return redirect(url_for('main.integrations'))


@integrations.route('/strava/webhook/endpoint', methods=['GET', 'POST'])
@csrf.exempt
def strava_webhook():
    """
        https://developers.strava.com/docs/webhooks
    """
    logging.info(request.get_json())
    data = request.get_json()
    # Process webhook
    process_strava_webhook(data)
    return Response(status=200)
