from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string

import logging

logger = logging.getLogger(__name__)

sensor_registry = {}


def get_sensor_class(path):
    return sensor_registry[path]


class Metering(AppConfig):
    name = 'metering'

    def ready(self, *args, **kwargs):
        sensor_class_list = getattr(settings, 'SENSORS', [])
        if sensor_class_list:
            import_string(sensor_class_list[0])
        for s in sensor_class_list:
            logger.info("Adding Sensor '%s'.." % s)
            sensor_registry[s] = import_string(s)
