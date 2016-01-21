from django.contrib import admin

from models import NivelSensor

# Register your models here.

@admin.register(NivelSensor)
class NivelSensorAdmin(admin.ModelAdmin):
    pass