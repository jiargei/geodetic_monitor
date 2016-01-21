from django.contrib import admin

from models import Sensor
# Register your models here.


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass