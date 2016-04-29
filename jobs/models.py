from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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
    last_completed = models.DateTimeField(null=True, blank=True, db_index=True)

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
        temp_time = timezone.localtime(timezone.now())

        if self.last_started is None:
            dt_task = float(self.frequency) * 60
        else:
            dt_task = (temp_time - self.last_started).total_seconds()

        if self.last_completed is None:
            dt_success = float(self.frequency) * 60
        else:
            dt_success = (temp_time - self.last_completed).total_seconds()

        dt_frequency = (temp_time - timezone.datetime(1970, 1, 1, tzinfo=timezone.get_current_timezone())).total_seconds()

        if self.active \
                and self.start_time <= temp_time.time() <= self.end_time \
                and (
                    (dt_task / 60.) >= self.frequency or
                    (dt_frequency % (60. * float(self.frequency))) <= 5 or
                    (dt_success / 60) >= self.frequency
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
