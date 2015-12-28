import datetime
from django.db import models

from bitfield import BitField

from lib import CONSTANTS


# Create your models here.


class TimeWindow(models.Model):
    von = models.TimeField()
    bis = models.TimeField()
    frequency = models.DecimalField(default=10., decimal_places=2, max_digits=5)
    # day_of_week = models.CharField(max_length=7, default="1234567")

    day_of_week = BitField(flags=(
        'Montag',
        'Dienstag',
        'Mittwoch',
        'Donnerstag',
        'Freitag',
        'Samstag',
        'Sonntag',
    ))

    def __unicode__(self):
        return u"%s - %s an %s, %s min" % (self.von, self.bis, self.day_of_week, self.frequency)


class Position(models.Model):
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    recent_sensor = models.ForeignKey("Sensor", blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s" % self.name


class Sensor(models.Model):
    name = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.serial_number)


class Task(models.Model):
    time_windows = models.ManyToManyField("TimeWindow")
    position = models.ForeignKey("Position")
    targets = models.ManyToManyField("Target")
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (self.position, self.targets, self.time_windows)

    class Meta:
        ordering = ["position"]
