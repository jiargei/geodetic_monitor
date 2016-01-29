from models import NivelSensor
from django.contrib import admin

# Register your models here.

@admin.register(NivelSensor)
class NivelSensorAdmin(admin.ModelAdmin):
    pass