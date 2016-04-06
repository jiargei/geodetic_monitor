from .apps import sensor_registry

def get_sensor_type_choices():
    return []


def get_sensor_model_choices():
    return sensor_registry.items()
