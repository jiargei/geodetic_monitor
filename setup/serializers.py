from django.forms import widgets

from rest_framework import serializers

import datetime

from tachy_control.models import TachySensor

from setup.models import Project, FipoTarget, SupoTarget
from setup.models import TachyPosition, TachyStation
from setup.models import FipoTask, FipoMeasurement
from setup.models import SupoTask, SupoMeasurement


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    tachypositions = serializers.HyperlinkedRelatedField(many=True,
                                                         read_only=True,
                                                         view_name='tachyposition-detail')
    fipotargets = serializers.HyperlinkedRelatedField(many=True,
                                                      read_only=True,
                                                      view_name='fipotarget-detail')
    supotargets = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                      view_name='supotarget-detail')

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = ('id', 'owner', 'name', 'token', 'description', 'active',
                  'tachypositions',
                  'fipotargets', 'supotargets')


class TachyPositionSerializer(serializers.HyperlinkedModelSerializer):

    active = serializers.BooleanField()
    use_stable = serializers.BooleanField()
    tachystations = serializers.HyperlinkedRelatedField(many=True,
                                                        read_only=True,
                                                        view_name='tachystation-detail')
    fipotasks = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='fipotask-detail')
    supotasks = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='supotask-detail')

    class Meta:
        model = TachyPosition
        fields = ('name', 'project', 'active', 'use_stable', 'tachystations', 'fipotasks', 'supotasks')


class TachyStationSerializer(serializers.HyperlinkedModelSerializer):
    fipomeasurements = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                           view_name='fipomeasurement-detail')
    supomeasurements = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                           view_name='supomeasurement-detail')
    class Meta:
        model = TachyStation
        fields = ('position', 'easting', 'northing', 'height', 'orientation',
                  'fipomeasurements', 'supomeasurements')


class FipoTargetSerializer(serializers.HyperlinkedModelSerializer):
    use_plane = serializers.BooleanField()
    use_height = serializers.BooleanField()
    fipotasks = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='fipotask-detail')
    fipomeasurements = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                           view_name='fipomeasurement-detail')
    class Meta:
        model = FipoTarget
        fields = ('project', 'name', 'prism',
                  'easting', 'northing', 'height',
                  'use_plane', 'use_height',
                  'fipotasks', 'fipomeasurements')


class SupoTargetSerializer(serializers.HyperlinkedModelSerializer):
    supotasks = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='supotask-detail')
    supomeasurements = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                           view_name='supomeasurement-detail')
    class Meta:
        model = SupoTarget
        fields = ('project', 'name', 'prism',
                  'easting', 'northing', 'height',
                  'supotasks', 'supomeasurements')


class FipoTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FipoTask
        fields = ('target', 'position', 'active',
                  'from_time', 'to_time' ,'frequency')


class TachyTaskSerializer(serializers.HyperlinkedModelSerializer):
    from_time = serializers.TimeField(default=datetime.time(0, 0, 0))
    frequency = serializers.FloatField(default=60.)


class SupoTaskSerializer(serializers.HyperlinkedModelSerializer):
    from_time = serializers.TimeField(default=datetime.time(0, 0, 0))
    frequency = serializers.FloatField(default=60.)
    active = serializers.BooleanField(default=True)
    class Meta:
        model = SupoTask
        fields = ('target', 'position', 'active',
                  'from_time', 'to_time' ,'frequency')


class FipoMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    horizontal_angle_corrected = serializers.SerializerMethodField()
    calculated_easting = serializers.SerializerMethodField()
    calculated_northing = serializers.SerializerMethodField()
    calculated_height = serializers.SerializerMethodField()
    difference_easting = serializers.SerializerMethodField()
    difference_northing = serializers.SerializerMethodField()
    difference_height = serializers.SerializerMethodField()
    
    class Meta:
        model = FipoMeasurement
        fields = ('created', 'station', 'target', 'face',
                  'horizontal_angle', 'horizontal_angle_corrected',
                  'vertical_angle', 'slope_distance',
                  'calculated_easting', 'calculated_northing', 'calculated_height',
                  'difference_easting', 'difference_northing', 'difference_height')

    def get_horizontal_angle_corrected(self, obj):
        # station = TachyStation.objects.get(id=obj.station)
        return (obj.horizontal_angle + obj.station.orientation) % 400

    def get_calculated_easting(self, obj):
        tmp = obj.station.polar_to_grid(obj.horizontal_angle,
                                        obj.vertical_angle,
                                        obj.slope_distance)
        return float(format(tmp['easting'], '.3f'))

    def get_calculated_northing(self, obj):
        tmp = obj.station.polar_to_grid(obj.horizontal_angle,
                                        obj.vertical_angle,
                                        obj.slope_distance)
        return float(format(tmp['northing'], '.3f'))

    def get_calculated_height(self, obj):
        tmp = obj.station.polar_to_grid(obj.horizontal_angle,
                                        obj.vertical_angle,
                                        obj.slope_distance)
        return float(format(tmp['height'], '.3f'))

    def get_difference_northing(self, obj):
        return float(format(self.get_calculated_northing(obj) - obj.target.northing, '.3f'))

    def get_difference_easting(self, obj):
        return float(format(self.get_calculated_easting(obj) - obj.target.easting, '.3f'))

    def get_difference_height(self, obj):
        return float(format(self.get_calculated_height(obj) - obj.target.height, '.3f'))

    
class SupoMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SupoMeasurement
        fields = ('created', 'station', 'target', 'face',
                  'horizontal_angle', 'vertical_angle', 'slope_distance')


