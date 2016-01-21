from django.contrib import admin

from sensors.tachy.admin import TachyTargetInline, TachyPositionInline
from .models import Project, Membership, Box, User

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

