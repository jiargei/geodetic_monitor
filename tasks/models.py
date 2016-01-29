from __future__ import unicode_literals

from bitfield import BitField

from common import fields
from django.db import models

# Create your models here.


class TimeWindow(models.Model):
    """

    """
    id = fields.IdField()
    active = models.BooleanField(default=True)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    frequency = models.DecimalField(default=10., max_digits=4, decimal_places=1)
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
        return "von %s, bis %s, alle %.1f Minten" % (self.start_time, self.end_time, self.frequency)


class Task(models.Model):
    """

    """
    id = fields.IdField()
    active = models.BooleanField(default=True)

