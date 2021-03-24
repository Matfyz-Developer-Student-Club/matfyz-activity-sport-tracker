from mast.models import User, Sex
from mast.queries import Queries
from mast import db
from math import ceil
from datetime import time


class Points(object):
    _DB_QUERY: Queries = None
    _FEMALE_COEFFICIENT: float = 1.1
    _MALE_COEFFICIENT: int = 1

    def __init__(self):
        super(object, self).__init__()
        self._DB_QUERY = Queries()

    def get_ride_activity_points(self, user: User, elevation: float, distance: float, pace: time) -> int:
        """
        This method gets for the given user and activity metadata points for this activity.
        :param user: Current User instance.
        :param elevation: Elevation of the activity in metres.
        :param distance: Distance of the activity in kilometres.
        :param pace: Pace in the minute per kilometres for the given activity.
        :return: Points for the Ride activity.
        """

        return self._get_points(user, elevation, distance, pace)

    def get_run_activity_points(self, user: User, elevation: float, distance: float, pace) -> int:
        """
        This method gets for the given user and activity metadata for this points.
        :param user: Current User instance.
        :param elevation: Elevation of the activity in metres.
        :param distance: Distance of the activity in kilometres.
        :param pace: Pace in the minute per kilometres for the given activity.
        :return: Points for the Run activity.
        """

        return self._get_points(user, elevation, distance, pace)

    def get_walk_activity_points(self, elevation: float, distance: float) -> int:
        """
        This method gets for the given user and activity metadata for this points.
        :param elevation: Elevation of the activity in metres.
        :param distance: Distance of the activity in kilometres.
        :return: Points for the Walk activity.
        """

        return ceil(distance * (1 + self._get_elevation(elevation, distance)))

    def get_inline_activity_points(self, elevation: float, distance: float) -> int:
        """
        This method gets for the given user and activity metadata for this points.
        :param elevation: Elevation of the activity in metres.
        :param distance: Distance of the activity in kilometres.
        :return: Points for the Inline activity.
        """

        return ceil(distance * (1 + self._get_elevation_percentage(elevation, distance)))

    @staticmethod
    def _get_elevation_percentage(height: float, distance: float) -> float:
        """
        This method gets percentage of the elevation from the given distance and height
        :param height: Elevation of the activity in metres.
        :param distance: Distance of the activity in kilometres.
        :return: Points for the Inline activity.
        """
        return height / (distance * 1000)

    @staticmethod
    def _get_user_sex(user: User) -> Sex:
        """
        Gets the user's sex.
        :param user: Current user.
        :return: User's sex
        """
        return User.query.filter_by(id=user.id).first().sex

    @staticmethod
    def _get_pace_percentage(pace: time) -> float:
        """
        Gets the method pace percentage based on the issued interval.
        :param pace: User's pace.
        :return: Percentage of the elevation.
        """
        pace_values = list(reversed(
            [time(minute=x // 2, second=30 if isinstance(x / 2, float) else 0) for x in range(5, 16)]))

        if pace < pace_values[0]:
            return 1

        if pace > pace_values[-1]:
            return 2

        for i in range(1, len(pace_values)):
            if pace_values[i - 1] <= pace <= pace_values[i]:
                return 1 + i / 10

    def _get_points(self, user: User, elevation: float, distance: float, pace: time) -> int:
        """
        Common method for evaluation of the point.
        :param elevation: Elevation of the activity in metres.
        :param distance: Distance of the activity in kilometres.
        :param pace: Pace in the minute per kilometres for the given activity.
        :return: Points for the given activity.
        """
        if Points._get_user_sex(user) == Sex.Female:
            return int((distance * (1 + Points._get_elevation_percentage(elevation,
                                                                         distance)) * self._FEMALE_COEFFICIENT) * Points._get_pace_percentage(
                pace) * 1000)

        return int(((distance * (1 + Points._get_elevation_percentage(elevation,
                                                                      distance)) * self._MALE_COEFFICIENT) * Points._get_pace_percentage(
            pace)) * 1000)
