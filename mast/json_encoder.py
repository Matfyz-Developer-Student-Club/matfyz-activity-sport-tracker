from mast.models import User, Competition, Sex, Age, Activity
from json import JSONEncoder
from datetime import time


class MastEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Activity):
            if obj.duration == time(0):
                duration = 'Not available'
            else:
                duration = None
            return {'datetime': obj.datetime.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S'),
                    'distance': obj.distance,
                    'duration': duration or obj.duration.strftime('%H:%M:%S'),
                    'average_duration_per_km': duration or obj.average_duration_per_km.strftime('%H:%M:%S'),
                    'type': obj.type.name}
        return JSONEncoder.default(self, obj)
