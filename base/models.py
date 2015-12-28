from __future__ import unicode_literals

from django.db import models

from libs import constants

# Create your models here.


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


class ObservationType(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    scale = models.FloatField(default=1)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.unit)


class Sensor(models.Model):
    name = models.CharField(max_length=40)
    serial_number = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.serial_number)