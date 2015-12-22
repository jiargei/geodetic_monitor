from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from base.models import Position, Coordinate, Target
from libs import constants

# Create your models here.


class TachyPosition(Position):
    pass


class TachyTarget(Target):
    target_type = models.CharField(default='d', max_length=1, choices=constants.TARGET_TYPE_CHOICES)
    prism_type = models.PositiveSmallIntegerField(choices=constants.PRISM_CHOICES, default=1)

    def __unicode__(self):
        return u"%s-%s (%s)" % (self.project.token, self.name, dict(constants.TARGET_TYPE_CHOICES).get(self.target_type))

    class Meta:
        ordering = ["target_type", "name"]


class TachyStation(Coordinate):
    position = models.ForeignKey("TachyPosition", on_delete=models.CASCADE)
    # sensor = models.ForeignKey("Sensor", on_delete=models.SET_NULL, null=True, blank=True)
    von = models.DateTimeField(default=datetime.now())
    bis = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.position.name)

    class Meta:
        ordering = ["position", "von"]

