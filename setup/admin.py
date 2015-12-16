from django.contrib import admin

from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield.admin import BitFieldListFilter

from setup.models import Project, Membership, Position, Station, Sensor, Target, Task, TimeWindow, Box
from setup.models import ObservationType, AlarmPlan, AlarmPhase, AlarmNotification, UserNotification, BoxNotification

# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
    # list_filter = (
    #     ('flags', BitFieldListFilter,)
    # )


class TimeWindowAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
    # list_filter = (
    #     ('flags', BitFieldListFilter,)
    # )


class AlarmPhaseInline(admin.TabularInline):
    model = AlarmPhase
    extra = 1


class AlarmPlanAdmin(admin.ModelAdmin):
    inlines = [AlarmPhaseInline]


admin.site.register(Box)
admin.site.register(Project)
admin.site.register(Membership)
admin.site.register(Position)
admin.site.register(Station)
admin.site.register(Sensor)

admin.site.register(Target)

admin.site.register(Task)
admin.site.register(TimeWindow, TimeWindowAdmin)

admin.site.register(ObservationType)
admin.site.register(AlarmPlan, AlarmPlanAdmin)
# admin.site.register(AlarmPhase)
admin.site.register(AlarmNotification)
admin.site.register(UserNotification, NotificationAdmin)
admin.site.register(BoxNotification, NotificationAdmin)
