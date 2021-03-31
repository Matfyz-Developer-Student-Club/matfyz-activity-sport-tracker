from flask import url_for, current_app
from mast import mail
from mast.models import Activity, User, ActivityType
from flask_mail import Message
from mast.queries import Queries
from datetime import time


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
        Distance: {activity.distance} km
        Duration: {activity.duration} hh:mm:ss
        Elevation: {activity.elevation} m
        Score: {activity.score} points
        
    
    Stay tuned and have a nice day!
    Your Mathletics team.
    '''
    mail.send(msg)


def get_statistics(activityType: ActivityType) ->list:
    db_query = Queries()
    activities = db_query.get_all_activities_by_type(activityType)

    statistics = _get_empty_statistics(activityType)
    if len(activities) > 0:
        statistics['MaxPace'], statistics['MinPace'], statistics['AvgPace'], statistics['MaxElev'],\
            statistics['MinElev'], statistics['AvgElev'], statistics['AvgDistance'],\
            statistics['AvgScore'] = _get_values(activities)

    return statistics


def _get_empty_statistics(activityType) ->dict:
    statistics = {
        'Category': activityType,
        'MaxPace': time(),
        'MinPace': time(),
        'AvgPace': time(),
        'MaxElev': 0,
        'MinElev': 0,
        'AvgElev': 0,
        'AvgDistance': 0,
        'AvgScore': 0
    }
    return statistics


def _get_values(activities):
    maxPace, minPace, avgPace = time(), time(), time()
    maxElev, minElev, avgElev, avgDistance, avgScore = 0, 0, 0, 0, 0

    totalSeconds = 0

    activity: Activity
    for activity in activities:
        # pace
        maxPace = max(maxPace, activity.average_duration_per_km)
        if minPace == time():
            minPace = activity.average_duration_per_km
        else:
            minPace = min(minPace, activity.average_duration_per_km)
        totalSeconds += _get_total_seconds(activity.average_duration_per_km)
        # elevation
        maxElev = max(maxElev, activity.elevation)
        minElev = min(maxElev, activity.elevation)
        avgElev += activity.elevation
        # distance
        avgDistance += activity.distance
        # score
        avgScore += activity.score

    avgScore //= len(activities)
    avgElev /= len(activities)
    avgDistance /= len(activities)
    totalSeconds //= len(activities)

    avgPace = _get_time_from_seconds(totalSeconds)

    return maxPace, minPace, avgPace, maxElev, minElev, avgElev, avgDistance, avgScore


def _get_total_seconds(pace:time):
    return pace.hour * 3600 + pace.minute * 60 + pace.second


def _get_time_from_seconds(seconds:int):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return time(hours, minutes, seconds)
