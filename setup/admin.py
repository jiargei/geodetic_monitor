from django.contrib import admin

from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from setup.models import Position, Station, Sensor, Target, Task, TimeWindow
from setup.models import ObservationType

# Register your models here.


class TimeWindowAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
    # list_filter = (
    #     ('flags', BitFieldListFilter,)
    # )

admin.site.register(Position)
admin.site.register(Station)
admin.site.register(Sensor)

admin.site.register(Target)

admin.site.register(Task)
admin.site.register(TimeWindow, TimeWindowAdmin)

admin.site.register(ObservationType)
