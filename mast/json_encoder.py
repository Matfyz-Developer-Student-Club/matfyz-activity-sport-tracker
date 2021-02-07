from mast.models import User, Competition, Sex, Age, Activity
from json import JSONEncoder
from datetime import datetime, time


class MastEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Activity):
            if obj.duration == time(0):
                duration = 'Not available'
            else:
                duration = None
            return {'datetime': obj.datetime,
                    'distance': obj.distance,
                    'duration': duration or obj.duration,
                    'average_duration_per_km': duration or obj.average_duration_per_km,
                    'type': obj.type.name}
        elif isinstance(obj, User):
            return obj.display()
        elif isinstance(obj, datetime):
            return obj.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, time):
            return obj.replace(microsecond=0).strftime('%H:%M:%S')
        return JSONEncoder.default(self, obj)
