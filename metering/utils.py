from .apps import sensor_registry


def get_sensor_type_choices():
    return []


def get_sensor_model_choices():
    return [(k, cls.get_name()) for k, cls in sensor_registry.items()]
