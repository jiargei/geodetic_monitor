from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import  utc

from common import constants
from common.fields import UIDField
from common.models import CreatedModifiedMixin

from .utils import get_sensor_type_choices, get_sensor_model_choices
from .apps import get_sensor_class


class ObservationType(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=20, choices=constants.OBSERVATION_TYPE_CHOICES, unique=True)
    unit = models.CharField(max_length=10, choices=constants.OBSERVATION_UNIT_CHOICES)
    description = models.CharField(max_length=200)
    scale = models.FloatField(default=1)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.unit)


class Sensor(models.Model):
    """

    """
    id = UIDField()
    sensor_name = models.CharField(max_length=100)
    sensor_serial = models.CharField(max_length=20, unique=True)
    sensor_model = models.CharField(db_index=True, blank=True, null=True,
                                   choices=get_sensor_model_choices(),
                                   max_length=80)


    def __unicode__(self):
        # return u"%s-%s" % (dict(constants.SENSOR_TYPE_CHOICES).get(self.sensor_type), self.sensor_name)
        return u"%s - %s" % (self.sensor_name, self.sensor_serial)

    def get_sensor_class(self):
        return get_sensor_class(self.sensor_model)


class Coordinate(models.Model):
    """

    """
    id = UIDField()
    easting = models.FloatField(null=True, blank=True, db_index=True)
    northing = models.FloatField(null=True, blank=True, db_index=True)
    height = models.FloatField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class Station(Coordinate):
    position = models.ForeignKey('metering.Position', related_name='stations')
    sensor = models.ForeignKey('metering.Sensor', related_name='stations')
    from_date = models.DateTimeField(default=utc.now, db_index=True)
    to_date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ['-from_date']
        get_latest_by = "from_date"



class Position(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=50)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    sensors = models.ManyToManyField(Sensor, through=Station)
    status = models.PositiveSmallIntegerField(default=constants.STATUS_ACTIVE,
                                              choices=constants.STATUS_CHOICES,
                                              db_index=True)
    sensor_type = models.CharField(db_index=True, blank=True, null=True,
                                   choices=get_sensor_type_choices(),
                                   max_length=16)

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)


class Reference(models.Model):
    # TODO
    # id = UIDField()
    position = models.ForeignKey(Position, related_name='references')
    target = models.ForeignKey('metering.Target', related_name='references')


class Target(Coordinate):
    """

    """
    name = models.CharField(max_length=20)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position, through=Reference)
    status = models.PositiveSmallIntegerField(default=constants.STATUS_ACTIVE,
                                              choices=constants.STATUS_CHOICES,
                                              db_index=True)

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)
