from django.contrib import admin

from .models import Sensor, ObservationType, Position


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(ObservationType)
class ObservationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
