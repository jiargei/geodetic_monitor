from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from libs import constants
from bitfield import BitField

# Create your models here.


class AlarmPlan(models.Model):
    name = models.CharField(max_length=50)
    observation_type = models.ForeignKey("base.ObservationType", on_delete=models.CASCADE)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.observation_type)


class AlarmPhase(models.Model):
    alarm_plan = models.ForeignKey("AlarmPlan", on_delete=models.CASCADE)
    state = models.SmallIntegerField(default=0, choices=constants.ALARM_STATES)
    value = models.FloatField()

    def __unicode__(self):
        return u"%s, %s, %s" % (self.alarm_plan, dict(constants.ALARM_STATES).get(self.state), self.value)

    class Meta:
        ordering = ["alarm_plan", "state"]


class UserNotification(models.Model):
    alarm_phase = models.ForeignKey("AlarmPhase", on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    notification_type = BitField(
        flags=(
            'SMS',
            'Voice',
            'EMail',
        )
    )


class BoxNotification(models.Model):
    alarm_phase = models.ForeignKey("AlarmPhase", on_delete=models.CASCADE)
    boxes = models.ManyToManyField("accounts.Box")
    notification_type = BitField(
        flags=(
            'Blinklicht',
        )
    )
