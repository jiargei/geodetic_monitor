from django.contrib import admin

from .models import Project, Membership, Box, Sensor

from alarm.models import UserNotification, BoxNotification
from tachy.admin import TachyTargetInline, TachyPositionInline

# Register your models here.


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, TachyPositionInline, TachyTargetInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    # inlines = [BoxNotification]
    pass


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass