from django.contrib import admin
from models import TimeWindow
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

# Register your models here.


class TimeWindowInline(admin.TabularInline):
    model = TimeWindow
    extra = 1
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

