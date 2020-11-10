from mast import db
from mast.models import User, Sex, Age, Activity, ActivityType, Competition, Season, ChallengePart
from sqlalchemy.sql import asc, func
import datetime as dt


class Queries(object):
    SEASON: Season

    def __init__(self):
        self.SEASON = db.session.query(Season).\
            filter(Season.start_date <= dt.date.today(),
                   Season.end_date >= dt.date.today()).\
            one()

    def _get_user_last_activities(self, user_id: int, activity_types: list,  number: int):
        """
        Returns the last activities of specified types by specified user.
        :param user_id: ID of user.
        :param activity_types: Types of activities we want to sum to total distance.
        :param number: Number of returned activities.
        :returns: List of last activities.
        """
        return db.session.query(Activity).\
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type.in_(activity_types)).\
            order_by(Activity.datetime.desc()).\
            limit(number).\
            all()

    def get_user_last_activities(self, user_id: int,  number: int):
        """
        Returns the last activities by specified user.
        :param user_id: ID of user.
        :param number: Number of returned activities.
        :returns: List of last activities.
        """
        return self._get_user_last_activities(user_id, [ActivityType.Run, ActivityType.Walk, ActivityType.Ride], number)

    def get_user_last_activities_on_feet(self, user_id: int,  number: int):
        """
        Returns the last run/walk activities by specified user.
        :param user_id: ID of user.
        :param number: Number of returned activities.
        :returns: List of last activities.
        """
        return self._get_user_last_activities(user_id, [ActivityType.Run, ActivityType.Walk], number)

    def get_user_last_activities_on_bike(self, user_id: int,  number: int):
        """
        Returns the last bike activities by specified user.
        :param user_id: ID of user.
        :param number: Number of returned activities.
        :returns: List of last activities.
        """
        return self._get_user_last_activities(user_id, [ActivityType.Ride], number)

    def save_new_user_activities(self, user_id: int, activity: Activity):
        """
        Saves new activity by user.
        :param user_id: ID of user.
        :param activity: New activity to be saved.
        """
        activity.user_id = user_id
        db.session.add(activity)
        db.session.commit()

    def get_best_run_activities_by_user(self, user_id: int, competition: Competition, number: int):
        """
        Returns the best run activity by a specified user in a specified competition.
        :param user_id: ID of user.
        :param competition: Competition where we want the best run.
        :param number: Number of returned activities.
        :returns: Activity instance for the best run.
        """
        return db.session.query(Activity).\
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type == ActivityType.Run,
                   Activity.distance >= competition.value).\
            order_by(Activity.average_duration_per_km.asc()).\
            limit(number).\
            all()

    def _get_total_distance_by_user(self, user_id: int, activity_types: list):
        """
        Returns the total distance taken by a specified user in a specified types of activity.
        :param user_id: ID of user.
        :param activity_types: Types of activities we want to sum to total distance.
        :returns: The total distance in kilometres.
        """
        return db.session.query(func.sum(Activity.distance)).\
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type.in_(activity_types)).\
            scalar()

    def get_total_distance_by_user_on_feet(self, user_id: int):
        """
        Returns the total run/walk distance taken by a specified user.
        :param user_id: ID of user.
        :returns: The total distance in kilometres.
        """
        return self._get_total_distance_by_user(user_id, [ActivityType.Run, ActivityType.Walk])

    def get_total_distance_by_user_on_bike(self, user_id: int):
        """
        Returns the total ride distance taken by a specified user.
        :param user_id: ID of user.
        :returns: The total distance in kilometres.
        """
        return self._get_total_distance_by_user(user_id, [ActivityType.Ride])

    def get_total_distances_by_user_in_last_days(self, user_id: int, days: int):
        """
        Returns the total distance taken by a specified user in last days.
        :param user_id: ID of user.
        :param days: Number of days for which the total distances are returned.
        :returns: The total distances for each day as dictionary.
        """
        last_day = dt.date.today()
        first_day = last_day - dt.timedelta(days=days - 1)
        query_result = db.session.query(func.date(Activity.datetime).label('day'),
                                        func.sum(Activity.distance).label('distance')).\
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= first_day,
                   func.date(Activity.datetime) <= last_day,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date).\
            group_by('day').\
            order_by(asc('day')).\
            all()

        result = {}
        for i in range(7):
            result[(first_day + dt.timedelta(days=i)).isoformat()] = 0

        for item in query_result:
            result[item.day.isoformat()] = item.distance

        return result

    def get_top_users_best_run(self, competition: Competition, sex: Sex, age: Age, number: int):
        """
        Returns top users in the best run activity in a specified competition, sex and age category.
        :param competition: Competition where we want top users for the best run.
        :param sex: Sex of users for the top users list.
        :param age: Age category of users for the top users list.
        :param number: Number of users in the top users list
        :returns: List of top users and their best run activity.
        """
        subquery = db.session.query(Activity.user_id.label('user_id'),
                                    func.min(Activity.average_duration_per_km).label('best_time')).\
            filter(func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type == ActivityType.Run,
                   Activity.distance >= competition.value).\
            group_by(Activity.user_id).\
            subquery(with_labels=True)
        return db.session.query(User, Activity).\
            select_from(User).\
            join(subquery, User.id == subquery.c.user_id).\
            join(Activity, db.and_(Activity.user_id == subquery.c.user_id,
                                   Activity.average_duration_per_km == subquery.c.best_time)).\
            filter(User.sex == sex,
                   User.age == age,
                   User.competing).\
            order_by(Activity.average_duration_per_km.asc()).\
            limit(number).\
            all()

    def _get_top_users_total_distance(self, number: int, activity_types: list):
        """
        Returns top users in the total distance in specified activity types.
        :param number: Number of users in the top users list.
        :param activity_types: Types of activities we want to sum to total distance.
        :returns: List of top users and their total distance.
        """
        subquery = db.session.query(Activity.user_id.label('user_id'),
                                    func.sum(Activity.distance).label('total_distance')).\
            filter(func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type.in_(activity_types)).\
            group_by(Activity.user_id).\
            subquery(with_labels=True)
        return db.session.query(User, subquery.c.total_distance).\
            select_from(User).\
            join(subquery, User.id == subquery.c.user_id).\
            filter(User.competing).\
            order_by(subquery.c.total_distance.desc()).\
            limit(number).\
            all()

    def get_top_users_total_distance_on_feet(self, number: int):
        """
        Returns top users in the total run/walk distance.
        :param number: Number of users in the top users list.
        :returns: List of top users and their total distance.
        """
        return self._get_top_users_total_distance(number, [ActivityType.Run, ActivityType.Walk])

    def get_top_users_total_distance_on_bike(self, number: int):
        """
        Returns top users in the total ride distance.
        :param number: Number of users in the top users list.
        :returns: List of top users and their total distance.
        """
        return self._get_top_users_total_distance(number, [ActivityType.Ride])

    def _get_global_total_distance(self, activity_types: list):
        """
        Returns the total distance by all users in specified activity types.
        :param activity_types: Types of activities we want to sum to total distance.
        :returns: The total distance in kilometres.
        """
        return db.session.query(func.sum(Activity.distance)).\
            filter(func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type.in_(activity_types)).\
            scalar()

    def get_global_total_distance_on_feet(self):
        """
        Returns the total run/walk distance by all users.
        :returns: The total distance in kilometres.
        """
        return self._get_global_total_distance([ActivityType.Run, ActivityType.Walk])

    def get_global_total_distance_on_bike(self):
        """
        Returns the total ride distance by all users.
        :returns: The total distance in kilometres.
        """
        return self._get_global_total_distance([ActivityType.Ride])

    def get_challenge_parts(self):
        """
        Returns the list of all parts of challenge.
        :returns: Dictionary containing names of check points and distances.
        """
        query_result = db.session.query(ChallengePart).\
            filter(ChallengePart.season_id == self.SEASON.id).\
            order_by(ChallengePart.order.asc()).\
            all()

        result = {}
        dist = 0
        for item in query_result:
            dist += item.distance
            result[dist] = item.target

        return result
