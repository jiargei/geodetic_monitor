from django.contrib import admin

from .models import Project, Membership, Box, Sensor, User

from alarm.models import UserNotification, BoxNotification
from tachy.admin import TachyTargetInline, TachyPositionInline

# Register your models here.


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class BoxInline(admin.TabularInline):
    model = Box
    extra = 1


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, TachyPositionInline, TachyTargetInline, BoxInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    # inlines = [BoxNotification]
    pass


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass
