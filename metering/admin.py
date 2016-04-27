from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Sensor, ObservationType, Position, Reference, Target, Station, Profile


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1


class StationInline(admin.TabularInline):
    model = Station
    extra = 1


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(ObservationType)
class ObservationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    inlines = [ReferenceInline, StationInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


class TargetRessource(ModelResource):
    project = Field(column_name=u'project',
                    widget=ForeignKeyWidget("accounts.Project", u'id'))

    class Meta:
        model = Target
        fields = (u'project', u'id', u'name', u'easting', u'northing', u'height', )
        import_id_fields = [u'id']


@admin.register(Target)
class TargetAdmin(ImportExportModelAdmin):
    resource_class = TargetRessource


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass