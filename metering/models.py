from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

from common import constants
from common.fields import UIDField
from common.models import CreatedModifiedMixin

from .utils import get_sensor_type_choices, get_sensor_model_choices
from .apps import get_sensor_class


class ObservationType(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=20, choices=constants.OBSERVATION_TYPE_CHOICES, unique=True)
    unit = models.CharField(max_length=10, choices=constants.OBSERVATION_UNIT_CHOICES)
    description = models.CharField(max_length=200)
    scale = models.FloatField(default=1)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.unit)


class Sensor(models.Model):
    """

    """
    id = UIDField()
    sensor_name = models.CharField(max_length=100)
    sensor_serial = models.CharField(max_length=20, unique=True)
    sensor_model = models.CharField(db_index=True, blank=True, null=True,
                                    choices=get_sensor_model_choices(),
                                    max_length=100)

    def __unicode__(self):
        # return u"%s-%s" % (dict(constants.SENSOR_TYPE_CHOICES).get(self.sensor_type), self.sensor_name)
        return u"%s - %s" % (self.sensor_name, self.sensor_serial)

    def get_sensor_class(self):
        return get_sensor_class(self.sensor_model)


class Coordinate(models.Model):
    """

    """
    id = UIDField()
    easting = models.FloatField(null=True, blank=True, db_index=True)
    northing = models.FloatField(null=True, blank=True, db_index=True)
    height = models.FloatField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    def get_point(self):
        return {'x': self.easting,
                'y': self.northing,
                'z': self.height}


class Station(Coordinate):
    position = models.ForeignKey('metering.Position', related_name='stations')
    sensor = models.ForeignKey('metering.Sensor', related_name='stations')
    box = models.ForeignKey('accounts.Box', related_name='box', blank=True, null=True)
    # port = models.FileField(upload_to='/dev/', blank=True, null=True)
    port = models.CharField(blank=True, null=True, max_length=32)
    from_date = models.DateTimeField(default=timezone.now, db_index=True)
    to_date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ['-from_date']
        get_latest_by = "from_date"

    def __unicode__(self):
        return u"%s, %s, %s" % (self.position, self.sensor, self.from_date)


class Position(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=50)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    sensors = models.ManyToManyField(Sensor, through=Station)
    status = models.PositiveSmallIntegerField(default=constants.STATUS_ACTIVE,
                                              choices=constants.STATUS_CHOICES,
                                              db_index=True)
    sensor_type = models.CharField(db_index=True, blank=True, null=True,
                                   choices=get_sensor_type_choices(),
                                   max_length=16)

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)


class Reference(models.Model):
    """
    
    """
    id = UIDField()
    position = models.ForeignKey(Position, related_name='references')
    target = models.ForeignKey('metering.Target', related_name='references')

    def __unicode__(self):
        return u"%s -> %s" % (self.position, self.target)


class Target(Coordinate):
    """

    """
    name = models.CharField(max_length=20)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position, through=Reference)
    status = models.PositiveSmallIntegerField(default=constants.STATUS_ACTIVE,
                                              choices=constants.STATUS_CHOICES,
                                              db_index=True)
    point_type = models.CharField(max_length=1, choices=constants.TARGET_TYPE_CHOICES, default='d')

    def __unicode__(self):
        return u"%s-%s" % (self.project.token, self.name)


class Profile(models.Model):
    """

    """
    id = UIDField()
    targets = models.ManyToManyField("metering.Target", related_name="profiles")
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey("accounts.Project")
    p1_easting = models.DecimalField(default=0., max_digits=10, decimal_places=3)
    p1_northing = models.DecimalField(default=0., max_digits=10, decimal_places=3)
    p2_easting = models.DecimalField(default=0., max_digits=10, decimal_places=3)
    p2_northing = models.DecimalField(default=0., max_digits=10, decimal_places=3)
