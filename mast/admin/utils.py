from flask import url_for, current_app
from mast import mail
from mast.models import Activity, User
from flask_mail import Message


def send_suspicious_activity_email(activity: Activity, user: User):
    msg = Message('Mathletics - Suspicious activity',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])

    msg.body = f'''Dear user,
    
    Your activity STRAVA ID: {activity.strava_id} - STRAVA NAME:{activity.name},
    was marked by the KTV authorities as a suspicious. Kindly requesting to verify
    that your activity is recorded correctly. If so, please contact the KTV to resolve
    this issue. 
    
    Activity data:
        Date of activity: {activity.datetime}
        Distance: {activity.distance}
        Duration: {activity.duration}
        Elevation: {activity.elevation}
        Score: {activity.score}
        
    
    Stay tuned and have a nice day!
    Your Mathletics team.
    '''
    mail.send(msg)
