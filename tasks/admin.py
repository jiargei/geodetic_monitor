from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from models import TimeWindow
from django.contrib import admin


# Register your models here.


class TimeWindowInline(admin.TabularInline):
    model = TimeWindow
    extra = 1
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

