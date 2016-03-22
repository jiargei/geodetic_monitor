from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from models import Task
from django.contrib import admin


# Register your models here.


class Task(admin.TabularInline):
    model = Task
    extra = 1
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

