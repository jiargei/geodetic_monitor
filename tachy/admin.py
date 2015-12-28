from django.contrib import admin

from tachy.models import TachyPosition, TachyTarget, TachyTask, TachySensor
from tasks.admin import TimeWindowInline

# Register your models here.


@admin.register(TachyTarget)
class TachyTargetAdmin(admin.ModelAdmin):
    pass


@admin.register(TachyPosition)
class TachyPositionAdmin(admin.ModelAdmin):
    pass


@admin.register(TachySensor)
class TachySensorAdmin(admin.ModelAdmin):
    pass


@admin.register(TachyTask)
class TachyTaskAdmin(admin.ModelAdmin):
    inlines = [TimeWindowInline]


class TachyPositionInline(admin.TabularInline):
    model = TachyPosition
    extra = 1


class TachyTargetInline(admin.TabularInline):
    model = TachyTarget
    extra = 1
