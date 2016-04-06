from django.contrib import admin
from .models import Sensor, ObservationType, Position, Reference, Target


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(ObservationType)
class ObservationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    inlines = [ReferenceInline]


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    pass