from mast.models import User, Sex
from mast.queries import Queries
from mast import db
from math import ceil
from datetime import time


class Points(object):
    _DB_QUERY = None
    _FEMALE_COEFFICIENT = 1.1
    _MALE_COEFFICIENT = 1

    def __init__(self):
        super(object, self).__init__()
        self._DB_QUERY = Queries()

    def get_ride_activity_points(self, user: User, elevation: float, distance: float, pace: time) -> int:
        current_points = self._DB_QUERY.get_user_total_points_for_ride(user.id)

        return _get_points(current_points, elevation, distance, pace)

    def get_run_activity_points(self, user: User, elevation: float, distance: float, pace) -> int:
        current_points = self._DB_QUERY.get_user_total_points_for_run(user.id)

        return _get_points(current_points, elevation, distance, pace)

    def get_walk_activity_points(self, user: User, elevation: float, distance: float) -> int:
        current_points = self._DB_QUERY.get_user_total_points_for_walk(user.id)

        return ceil(current_points + (distance * (1 + self._get_elevation(elevation, distance))))

    def get_inline_activity_points(self, user: User, elevation: float, distance: float) -> int:
        current_points = self._DB_QUERY.get_user_total_points_for_inline(user.id)

        return ceil(current_points + (distance * (1 + self._get_elevation_percentage(elevation, distance))))

    @staticmethod
    def _get_elevation_percentage(elevation: float, distance: float) -> float:
        return elevation / (distance * 1000)

    @staticmethod
    def _get_user_sex(user: User) -> Sex:
        return User.query.filter_by(id=user.id).first().sex

    @staticmethod
    def _get_pace_percentage(pace: time) -> float:
        pace_values = list(reversed(
            [time(minute=x // 2, second=30 if isinstance(x / 2, float) else 0) for x in range(5, 16)]))

        if pace < pace_values[0]:
            return 1

        if pace > pace_values[-1]:
            return 2

        for i in range(1, len(pace_values)):
            if pace_values[i - 1] <= pace <= pace_values[i]:
                return 1 + i / 10

    def _get_points(self, current_points: int, elevation: float, distance: float, pace: time) -> int:
        if _get_user_sex(user) == Sex.Female:
            return ceil(
                current_points + (
                        distance * (1 + self._get_elevation(elevation,
                                                            distance)) * self._FEMALE_COEFFICIENT) * _get_pace_percentage(
                    pace))
        return ceil(
            current_points + (
                    distance * (1 + self._get_elevation(elevation,
                                                        distance)) * self._MALE_COEFFICIENT) * _get_pace_percentage(
                pace))
