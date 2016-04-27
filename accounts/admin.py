from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count


from .models import Project, Membership, Box, User


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class BoxInline(admin.TabularInline):
    model = Box
    extra = 1


@admin.register(User)
class MyUserAdmin(UserAdmin):
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
    list_display = ('user', 'role', 'project', 'created')
    list_select_related = ('user', 'project')
    list_filter = ('role', 'created')
    search_fields = ('user__username', 'project__name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'creator')
    inlines = [MembershipInline, BoxInline]
    list_filter = ('created',)
    search_fields = ('name', 'creator__username')


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'created', 'creator')
    list_select_related = ('project', 'creator')
    list_filter = ('created',)
    search_fields = ('name', 'project__name', 'creator__username')

