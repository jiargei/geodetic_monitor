from sensors.tachy.models import TachyPosition, TachyTarget, TachyTask, TachySensor, TachyStation
from django.contrib import admin
from tasks.admin import TimeWindowInline

# Register your models here.


class TachyPositionInline(admin.TabularInline):
    model = TachyPosition
    extra = 1


class TachyStationInline(admin.TabularInline):
    model = TachyStation
    extra = 1


class TachyTargetInline(admin.TabularInline):
    model = TachyTarget
    extra = 1


@admin.register(TachyTarget)
class TachyTargetAdmin(admin.ModelAdmin):
    pass


@admin.register(TachyPosition)
class TachyPositionAdmin(admin.ModelAdmin):
    inlines = [TachyStationInline]


@admin.register(TachySensor)
class TachySensorAdmin(admin.ModelAdmin):
    pass


@admin.register(TachyTask)
class TachyTaskAdmin(admin.ModelAdmin):
    inlines = [TimeWindowInline]
