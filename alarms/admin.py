from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from models import AlarmPlan, AlarmPhase, UserNotification, BoxNotification
from django.contrib import admin


# Register your models here.


@admin.register(BoxNotification)
class BoxNotificationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


class AlarmPhaseInline(admin.TabularInline):
    model = AlarmPhase
    extra = 1


@admin.register(AlarmPlan)
class AlarmPlanAdmin(admin.ModelAdmin):
    inlines = [AlarmPhaseInline]

