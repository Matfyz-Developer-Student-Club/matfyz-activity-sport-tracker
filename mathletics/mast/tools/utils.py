from flask_login import login_user, current_user
from mast import session


def check_profile_verified(session_data: session.Session):
    if not current_user.is_completed():
        session_data.error('Your profile is not completed! Please, go to Settings and fill in your data.<br />' +
                           'Your activities will be considered only after your profile is verified.')
    elif not current_user.verified:
        session_data.warning('Your profile is not yet verified. ' +
                             'Let us know if you are sure you filled in correct data and it takes too long.<br />' +
                             'Your activities will be considered only after your profile is verified.')



