from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from base.models import Position, Coordinate, Target, Sensor
from libs import constants
from tasks.models import Task
from .lib import constants as tc


# Create your models here.


class TachyPosition(Position):
    def __unicode__(self):
        return u"%s-TACHY-%s" % (self.project.token, self.name)


class TachyTarget(Target):
    target_type = models.CharField(default='d', max_length=1, choices=constants.TARGET_TYPE_CHOICES)
    prism_type = models.PositiveSmallIntegerField(choices=constants.PRISM_CHOICES, default=1)

    def __unicode__(self):
        return u"%s-TACHY-%s (%s)" % (self.project.token, self.name, dict(constants.TARGET_TYPE_CHOICES).get(self.target_type))

    class Meta:
        ordering = ["target_type", "name"]


class TachyStation(Coordinate):
    position = models.ForeignKey("TachyPosition", on_delete=models.CASCADE)
    # sensor = models.ForeignKey("Sensor", on_delete=models.SET_NULL, null=True, blank=True)
    von = models.DateTimeField(default=datetime.now())
    bis = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.position.name)

    def set_station(self):
        pass

    class Meta:
        ordering = ["position", "von"]


class TachyTask(Task):
    position = models.ForeignKey("TachyPosition", on_delete=models.CASCADE)
    targets = models.ManyToManyField("TachyTarget")

    def __unicode__(self):
        target_names = ""
        for target in self.targets.all():
            target_names += ", %s" % target.name

        return "%s: %s" % (self.position, self.targets)

        # def save(self, *args, **kwargs):
        #     """
        #     Checks if there is only one Task for each target
        #
        #     :param args:
        #     :param kwargs:
        #     :return:
        #     """
        #     target_found = False
        #     target_list = []
        #
        #     for target in self.targets.all():
        #         target_was_found = TachyTask.objects.filter(targets__pk=target.pk).count()
        #
        #         if target_was_found:
        #             target_list.append(target)
        #             target_found = True
        #
        #     if target_found:
        #         print "Element kann nicht gespeichert werden, folgende Ziele sind bereits vorhanden:"
        #         for target in target_list:
        #             print "- %s" % target
        #     else:
        #         super(TachyTask).save(*args, **kwargs)


class TachySensor(Sensor):
    model_type = models.PositiveSmallIntegerField(choices=tc.MODEL_TYPE_CHOICE, default=11)
