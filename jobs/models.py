from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import datetime

from bitfield import BitField

from accounts.models import Project
from common.fields import UIDField


class PeriodicTask(models.Model):
    """

    """
    id = UIDField()
    project = models.ForeignKey(Project)
    active = models.BooleanField(default=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    frequency = models.DecimalField(default=10., max_digits=4, decimal_places=1)
    last_started = models.DateTimeField(null=True, blank=True, db_index=True)

    day_of_week = BitField(flags=(
        ("0", _('monday')),
        ("1", _('tuesday')),
        ("2", _('wednesday')),
        ("3", _('thursday')),
        ("4", _('friday')),
        ("5", _('saturday')),
        ("6", _('sunday')),
    ))

    object_id = models.CharField(max_length=10, db_index=True)
    content_type = models.ForeignKey(ContentType)
    task_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    def __unicode__(self):
        return u"von %s, bis %s, alle %s Minuten" % (
            self.start_time, self.end_time, self.frequency
        )

    def is_due(self):
        """

        :return: True, if task should be executed, else False
        :rtype: bool
        """

        dt1 = (timezone.now() - self.last_started).total_seconds()
        dt0 = (timezone.now() - datetime.datetime(1970,1,1)).total_seconds()

        if self.active \
                and self.start_time <= timezone.now() <= self.end_time \
                and (
                        (dt1.total_seconds() / 60.) >= self.frequency
                        or (dt0 % (60. * float(self.frequency))) <= 5
                ):
            return True
        return False


class Task(models.Model):
    """

    """
    id = UIDField()

    def is_due(self):
        """

        :return: True, if task should be executed, else False
        :rtype: bool
        """
        return False
