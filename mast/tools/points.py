from mast.models import User
from mast.queries import Queries


class Points(object):
    _DB_QUERY = None

    def __init__(self):
        super(object, self).__init__()
        self._DB_QUERY = Queries

    def get_ride_activity_points(self, user: User, altitude: float, distance: float, pace) -> int:
        pass

    def get_run_activity_points(self, user: User, altitude: float, distance: float, pace) -> int:
        pass

    def get_walk_activity_points(self, user: User, altitude: float, distance: float, pace) -> int:
        pass

    def get_inline_activity_points(self, user: User, altitude: float, distance: float, pace) -> int:
        pass
