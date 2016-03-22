from __future__ import unicode_literals

from bitfield import BitField

from accounts.models import User
from common import constants
from common.fields import UIDField

from django.db import models

# Create your models here.


class AlarmPlan(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=50)
    observation_type = models.ForeignKey("metering.ObservationType", on_delete=models.CASCADE)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.observation_type)


class AlarmPhase(models.Model):
    """

    """
    id = UIDField()
    alarm_plan = models.ForeignKey("AlarmPlan", on_delete=models.CASCADE)
    state = models.SmallIntegerField(default=0, choices=constants.ALARM_STATES)
    value = models.FloatField()

    def __unicode__(self):
        return u"%s, %s, %s" % (self.alarm_plan, dict(constants.ALARM_STATES).get(self.state), self.value)

    class Meta:
        ordering = ["alarm_plan", "state"]


class UserNotification(models.Model):
    """

    """
    id = UIDField()
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
    """

    """
    id = UIDField()
    alarm_phase = models.ForeignKey("AlarmPhase", on_delete=models.CASCADE)
    boxes = models.ManyToManyField("accounts.Box")
    notification_type = BitField(
        flags=(
            'Blinklicht',
        )
    )
