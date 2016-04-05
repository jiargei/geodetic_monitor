from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string



class Metering(AppConfig):
    name = 'metering'

    def ready(self, *args, **kwargs):
        return
        for s in getattr(settings, 'SENSORS', []):
            import_string(s)

