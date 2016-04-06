from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string

sensor_registry = {}

def get_sensor_class(path):
    return sensor_registry[path]


class Metering(AppConfig):
    name = 'metering'

    def ready(self, *args, **kwargs):
        for s in getattr(settings, 'SENSORS', []):
            sensor_registry[s] = import_string(s)

