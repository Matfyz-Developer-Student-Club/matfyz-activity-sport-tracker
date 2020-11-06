from mast import db
from mast.models import User, Activity, ActivityType, Competition
from sqlalchemy.sql import asc, func, cast
from datetime import date, timedelta


def get_best_run_activity_by_user(user_id: int, competition: Competition):
    """
    Returns the best run activity by a specified user in a specified competition.
    :param user_id: ID of user.
    :param competition: Competition where we want the best run.
    :returns: Activity instance for the best run.
    """
    return db.session.query(Activity).\
        filter(Activity.user_id == user_id,
               Activity.type == ActivityType.Run,
               Activity.distance >= competition.value).\
        order_by(Activity.average_duration_per_km.asc()).\
        first()


def get_total_distance_by_user(user_id: int, activity_type: ActivityType):
    """
    Returns the total distance taken by a specified user in a specified type of activity.
    :param user_id: ID of user.
    :param activity_type: Type of activity for which we want the total distance.
    :returns: The total distance in kilometres.
    """
    return db.session.query(func.sum(Activity.distance)).\
        filter(Activity.user_id == user_id,
               Activity.type == activity_type).\
        scalar()


def get_total_distances_by_user_in_last_days(user_id: int, days: int):
    """
    Returns the total distance taken by a specified user in last days.
    :param user_id: ID of user.
    :param days: Number of days for which the total distances are returned.
    :returns: The total distances for each day.
    """
    return db.session.query(func.date(Activity.datetime).label("date"),
                            func.sum(Activity.distance).label("distance")).\
        filter(Activity.user_id == user_id,
               func.date(Activity.datetime) > date.today()-timedelta(days=days)).\
        group_by("date").\
        order_by(asc("date")).\
        all()
