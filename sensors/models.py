from __future__ import unicode_literals

from common import constants
from common.fields import UIDField
from common.models import CreatedModifiedMixin
from django.db import models

# Create your models here.


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
    # sensor_type = models.PositiveSmallIntegerField(default=1, choices=constants.SENSOR_TYPE_CHOICES)

    def __unicode__(self):
        # return u"%s-%s" % (dict(constants.SENSOR_TYPE_CHOICES).get(self.sensor_type), self.sensor_name)
        return u"%s - %s" % (self.sensor_name, self.sensor_serial)


class Coordinate(models.Model):
    """

    """
    id = UIDField()
    easting = models.FloatField()
    northing = models.FloatField()
    height = models.FloatField()

    class Meta:
        abstract = True


class Station(Coordinate):
    postion = models.ForeignKey('sensors.Position')
    sensor = models.ForeignKey('sensors.Sensor')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()


class Position(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=50)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    sensors = models.ManyToManyField(Sensor, through=Station)

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)


class Reference(models.Model):
    position = models.ForeignKey(Position)
    target = models.ForeignKey('sensors.Target')


class Target(Coordinate):
    """

    """
    name = models.CharField(max_length=20)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position, through=Reference)

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)
