from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from models import Task
from django.contrib import admin


# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
