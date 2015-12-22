from django.contrib import admin

from tachy.models import TachyPosition, TachyTarget

# Register your models here.


@admin.register(TachyTarget)
class TachyTargetAdmin(admin.ModelAdmin):
    pass


class TachyPositionInline(admin.TabularInline):
    model = TachyPosition
    extra = 1


class TachyTargetInline(admin.TabularInline):
    model = TachyTarget
    extra = 1
