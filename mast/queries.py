from mast import db
from mast.models import User, Sex, Age, UserType, Activity, ActivityType, Competition, Season, ChallengePart
from sqlalchemy.sql import asc, func
import datetime as dt


class Queries(object):
    SEASON: Season

    def __init__(self):
        self.SEASON = db.session.query(Season). \
            filter(Season.start_date <= dt.date.today(),
                   Season.end_date >= dt.date.today()). \
            first()
        if self.SEASON is None:
            self.SEASON = db.session.query(Season). \
                filter(Season.start_date > dt.date.today()). \
                order_by(Season.start_date.asc()). \
                first()
        if self.SEASON is None:
            self.SEASON = Season(title='', start_date=dt.date.today(), end_date=dt.date.today())

    def _get_user_last_activities(self, user_id: int, activity_types: list, number: int, offset: int = 0):
        """
        Returns the last activities of specified types by specified user.
        :param user_id: ID of user.
        :param activity_types: Types of activities we want to sum to total distance.
        :param number: Number of returned activities.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of activities and list of last activities.
        """
        query = db.session.query(Activity). \
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type.in_(activity_types))
        count = query. \
            count()
        items = query. \
            limit(number). \
            offset(offset). \
            all()
        return [count, items]

    def get_user_last_activities(self, user_id: int, number: int, offset: int = 0):
        """
        Returns the last activities by specified user.
        :param user_id: ID of user.
        :param number: Number of returned activities.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of activities and list of last activities.
        """
        return self._get_user_last_activities(user_id,
                                              [ActivityType.Run, ActivityType.Walk, ActivityType.Ride],
                                              number, offset)

    def get_user_last_activities_on_foot(self, user_id: int, number: int, offset: int = 0):
        """
        Returns the last run/walk activities by specified user.
        :param user_id: ID of user.
        :param number: Number of returned activities.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of activities and list of last activities.
        """
        return self._get_user_last_activities(user_id,
                                              [ActivityType.Run, ActivityType.Walk],
                                              number, offset)

    def get_user_last_activities_on_bike(self, user_id: int, number: int, offset: int = 0):
        """
        Returns the last bike activities by specified user.
        :param user_id: ID of user.
        :param number: Number of returned activities.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of activities and list of last activities.
        """
        return self._get_user_last_activities(user_id,
                                              [ActivityType.Ride],
                                              number, offset)

    def save_new_user_activities(self, user_id: int, activity: Activity):
        """
        Saves new activity by user.
        :param user_id: ID of user.
        :param activity: New activity to be saved.
        """
        activity.user_id = user_id
        db.session.add(activity)
        db.session.commit()

    def get_best_run_activities_by_user(self, user_id: int, competition: Competition, number: int, offset: int = 0):
        """
        Returns the best run activity by a specified user in a specified competition.
        :param user_id: ID of user.
        :param competition: Competition where we want the best run.
        :param number: Number of returned activities.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of activities and list of best activities.
        """
        query = db.session.query(Activity). \
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type == ActivityType.Run,
                   Activity.distance >= competition.value). \
            order_by(Activity.average_duration_per_km.asc())
        count = query. \
            count()
        items = query. \
            limit(number). \
            offset(offset). \
            all()
        return [count, items]

    def _get_total_distance_by_user(self, user_id: int, activity_types: list):
        """
        Returns the total distance taken by a specified user in a specified types of activity.
        :param user_id: ID of user.
        :param activity_types: Types of activities we want to sum to total distance.
        :returns: The total distance in kilometres.
        """
        return db.session.query(func.sum(Activity.distance)). \
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type.in_(activity_types)). \
            scalar()

    def get_total_distance_by_user_on_foot(self, user_id: int):
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
                                        func.sum(Activity.distance).label('distance')). \
            filter(Activity.user_id == user_id,
                   func.date(Activity.datetime) >= first_day,
                   func.date(Activity.datetime) <= last_day,
                   func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date). \
            group_by('day'). \
            order_by(asc('day')). \
            all()

        result = {}
        for i in range(7):
            result[(first_day + dt.timedelta(days=i)).isoformat()] = 0

        for item in query_result:
            result[item.day] = item.distance

        return result

    def _get_top_users_best_run_subquery(self, competition: Competition):
        """
        Returns subquery for top users in the best run activity in a specified competition.
        :param competition: Competition where we want top users for the best run.
        :returns: Subquery returning user_id and id for user´s best run.
        """
        best_times = db.session.query(Activity.user_id.label('user_id'),
                                      func.min(Activity.average_duration_per_km).label('best_time')). \
            filter(func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type == ActivityType.Run,
                   Activity.distance >= competition.value). \
            group_by(Activity.user_id). \
            subquery(with_labels=True)
        return db.session.query(Activity.user_id.label('user_id'),
                                            func.min(Activity.id).label('id')). \
            select_from(Activity). \
            join(best_times, db.and_(Activity.user_id == best_times.c.user_id,
                                     Activity.average_duration_per_km == best_times.c.best_time)). \
            filter(func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type == ActivityType.Run,
                   Activity.distance >= competition.value). \
            group_by(Activity.user_id). \
            subquery(with_labels=True)

    def get_top_users_best_run(self, competition: Competition, sex: Sex, age: Age, number: int, offset: int = 0):
        """
        Returns top users in the best run activity in a specified competition, sex and age category.
        :param competition: Competition where we want top users for the best run.
        :param sex: Sex of users for the top users list.
        :param age: Age category of users for the top users list.
        :param number: Number of users in the top users list
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of users and list of top users and their best run activity.
        """
        best_times = self._get_top_users_best_run_subquery(competition)
        query = db.session.query(User, Activity). \
            select_from(User). \
            join(best_times, User.id == best_times.c.user_id). \
            join(Activity, db.and_(Activity.user_id == best_times.c.user_id,
                                   Activity.id == best_times.c.id)). \
            filter(User.sex == sex,
                   User.age == age,
                   User.competing,
                   User.verified). \
            order_by(Activity.average_duration_per_km.asc())
        count = query. \
            count()
        items = query. \
            limit(number). \
            offset(offset). \
            all()
        return [count, items]

    def _get_top_users_total_distance_subquery(self, activity_types: list):
        """
        Returns subquery for top users in the total distance in specified activity types.
        :param activity_types: Types of activities we want to sum to total distance.
        :returns: Subquery returning user_id and total distance.
        """
        return db.session.query(Activity.user_id.label('user_id'),
                                    func.sum(Activity.distance).label('total_distance')). \
            filter(func.date(Activity.datetime) >= self.SEASON.start_date,
                   func.date(Activity.datetime) <= self.SEASON.end_date,
                   Activity.type.in_(activity_types)). \
            group_by(Activity.user_id). \
            subquery(with_labels=True)

    def _get_top_users_total_distance(self, activity_types: list, number: int, offset: int = 0):
        """
        Returns top users in the total distance in specified activity types.
        :param activity_types: Types of activities we want to sum to total distance.
        :param number: Number of users in the top users list.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of users and list of top users and their total distance.
        """
        total_distances = self._get_top_users_total_distance_subquery(activity_types)
        query = db.session.query(User, total_distances.c.total_distance). \
            select_from(User). \
            join(total_distances, User.id == total_distances.c.user_id). \
            filter(User.competing,
                   User.verified). \
            order_by(total_distances.c.total_distance.desc())
        count = query. \
            count()
        items = query. \
            limit(number). \
            offset(offset). \
            all()
        return [count, items]

    def get_top_users_total_distance_on_foot(self, number: int, offset: int = 0):
        """
        Returns top users in the total run/walk distance.
        :param number: Number of users in the top users list.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of users and list of top users and their total distance.
        """
        return self._get_top_users_total_distance([ActivityType.Run, ActivityType.Walk], number, offset)

    def get_top_users_total_distance_on_bike(self, number: int, offset: int = 0):
        """
        Returns top users in the total ride distance.
        :param number: Number of users in the top users list.
        :param offset: Offset of returned activities - default: 0.
        :returns: Total count of users and list of top users and their total distance.
        """
        return self._get_top_users_total_distance([ActivityType.Ride], number, offset)

    def _get_global_total_distance(self, activity_types: list):
        """
        Returns the total distance by all users in specified activity types.
        :param activity_types: Types of activities we want to sum to total distance.
        :returns: The total distance in kilometres.
        """
        return db.session.query(func.sum(Activity.distance)). \
                   select_from(User). \
                   join(User.activities). \
                   filter(func.date(Activity.datetime) >= self.SEASON.start_date,
                          func.date(Activity.datetime) <= self.SEASON.end_date,
                          Activity.type.in_(activity_types),
                          User.verified). \
                   scalar() or 0

    def get_global_total_distance_on_foot(self):
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

    def _get_challenge_parts(self):
        """
        Returns the list of all parts of challenge.
        :returns: Dictionary containing names of check points and distances.
        """
        query_result = db.session.query(ChallengePart). \
            filter(ChallengePart.season_id == self.SEASON.id). \
            order_by(ChallengePart.order.asc()). \
            all()

        result = {}
        dist = 0
        for item in query_result:
            dist += item.distance
            result[dist] = item.target

        return result

    def get_challenge_parts_to_display(self):
        """
        Returns the list of all parts of challenge to be displayed -
        all completed parts, current part and one more (if present).
        :returns: Dictionary containing names of check points and distances.
        """
        dist = max(self.get_global_total_distance_on_foot(), self.get_global_total_distance_on_bike())
        checkpoints = self._get_challenge_parts()

        result = {}
        one_more = True
        for d, target in checkpoints.items():
            if d <= dist:
                result[d] = target
            elif one_more:
                result[d] = target
                one_more = False
            else:
                result[d] = target
                break
        return result

    def get_current_challenge_part(self):
        """
        Returns the order number of current part of challenge -
        the one where the better of on foot / on bike challenge is.
        :returns: String representing the order number.
        """
        dist = max(self.get_global_total_distance_on_foot(), self.get_global_total_distance_on_bike())
        checkpoints = self._get_challenge_parts()

        result = 0
        for d in checkpoints.keys():
            if d <= dist:
                result = result + 1

        return '%02d' % result

    def get_stats(self):
        """
        Returns the statistics about users.
        :returns: Object containing the statistics.
        """
        result = {
            'datetime': dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            'total': db.session.query(User).\
                count(),
            'unverified': db.session.query(User).\
                filter(db.not_(User.verified)).\
                count(),
            'male students': db.session.query(User).\
                filter(User.sex == Sex.Male,
                       User.type == UserType.Student).\
                count(),
            'male employees': db.session.query(User).\
                filter(User.sex == Sex.Male,
                       User.type == UserType.Employee).\
                count(),
            'male alumni': db.session.query(User).\
                filter(User.sex == Sex.Male,
                       User.type == UserType.Alumni).\
                count(),
            'female students': db.session.query(User).\
                filter(User.sex == Sex.Female,
                       User.type == UserType.Student).\
                count(),
            'female employees': db.session.query(User).\
                filter(User.sex == Sex.Female,
                       User.type == UserType.Employee).\
                count(),
            'female alumni': db.session.query(User).\
                filter(User.sex == Sex.Female,
                       User.type == UserType.Alumni).\
                count()
        }

        return result
