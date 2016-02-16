from django.contrib import admin

from .models import Sensor, ObservationType


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(ObservationType)
class ObservationTypeAdmin(admin.ModelAdmin):
    pass
