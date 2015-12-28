from __future__ import unicode_literals

from django.db import models
from bitfield import BitField

# Create your models here.


class TimeWindow(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    frequency = models.DecimalField(default=10., decimal_places=3, max_digits=7)
    day_of_week = BitField(flags=(
        'Montag',
        'Dienstag',
        'Mittwoch',
        'Donnerstag',
        'Freitag',
        'Samstag',
        'Sonntag',
    ))


class Task(models.Model):
    active = models.BooleanField(default=True)
