from __future__ import unicode_literals

from django.db import models

from common import constants

# Create your models here.


class ObservationType(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    scale = models.FloatField(default=1)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.unit)


class Sensor(models.Model):
    sensor_name = models.CharField(max_length=100)
    sensor_serial = models.CharField(max_length=20, unique=True)
    # sensor_type = models.PositiveSmallIntegerField(default=1, choices=constants.SENSOR_TYPE_CHOICES)

    def __unicode__(self):
        # return u"%s-%s" % (dict(constants.SENSOR_TYPE_CHOICES).get(self.sensor_type), self.sensor_name)
        return u"%s - %s" % (self.sensor_name, self.sensor_serial)


class Coordinate(models.Model):
    easting = models.FloatField()
    northing = models.FloatField()
    height = models.FloatField()

    class Meta:
        abstract = True


class PositionMembership(models.Model):
    position = models.OneToOneField("accounts.Project", on_delete=models.CASCADE)


class Position(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)


class Target(Coordinate):
    name = models.CharField(max_length=20)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)
