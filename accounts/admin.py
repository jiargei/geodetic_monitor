from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

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
class CustomUserAdmin(UserAdmin):
    inlines = [MembershipInline]
    list_display = UserAdmin.list_display + ('num_memberships',)

    def get_queryset(self, *args, **kwargs):
        qs = super(UserAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(num_memberships=Count('memberships'))
        return qs

    def num_memberships(self, obj):
        return obj.num_memberships
    num_memberships.admin_order_field = 'num_memberships'
    num_memberships.short_description = 'number of memberships'


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'project')
    list_select_related = ('user', 'project')
    list_filter = ('role',)
    search_fields = ('user__username', 'project__name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, TachyPositionInline, TachyTargetInline, BoxInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    # inlines = [BoxNotification]
    pass

