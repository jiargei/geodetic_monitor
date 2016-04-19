from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from .models import PeriodicTask
from django.contrib import admin


# Register your models here.


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


