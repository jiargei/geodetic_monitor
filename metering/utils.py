from .apps import sensor_registry
from django.conf import settings
import logging
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def get_sensor_type_choices():
    return []


def get_sensor_model_choices():
    sensor_class_list = getattr(settings, 'SENSORS', [])
    if sensor_class_list:
        import_string(sensor_class_list[0])
    for s in sensor_class_list:
        logger.debug("Adding Sensor '%s'.." % s)
        sensor_registry[s] = import_string(s)
    # print "Sensor Registry: ", sensor_registry
    return [(k, cls.get_name()) for k, cls in sensor_registry.items()]
