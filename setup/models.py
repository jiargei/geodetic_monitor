from django.db import models

from lib import geodetic

import datetime

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    token = models.CharField(max_length=10, default='')
    active = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', related_name='projects')

    def __unicode__(self):
        return "%s - %s" % (self.token, self.name)


class Coordinate(models.Model):
    easting = models.FloatField()
    northing = models.FloatField()
    height = models.FloatField()

    class Meta:
        abstract = True


class TachyPosition(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project,
                                related_name="%(class)ss")
    active = models.BooleanField(default=True)
    use_stable = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.name


class TachyStation(Coordinate):
    position = models.ForeignKey(TachyPosition, related_name="tachystations")
    orientation = models.FloatField(default=0.0)
    stable = models.BooleanField(default=True)

    def polar_to_grid(self, hz, v, sd):
        """
        Haengt Beobachtung zu Zielpunkt an Standpunkt an
        :param hz: Richtungswinkel zu Zielpunkt in GON
        :type hz: float
        :param v: Vertikalwinkel zu Zielpunkt in GON
        :type v: float
        :param sd: Schraegdistanz zu Zielpunkt
        :type sd: float
        :return: easting, northin, height
        :rtype: dict
        """
        return geodetic.polar_to_grid(self.easting, self.northing, self.height,
                                      hz, self.orientation, v, sd)

    def __unicode__(self):
        return "%s, %.4f" % (self.position, self.orientation)


class TachyTarget(Coordinate):
    project = models.ForeignKey(Project, 
                                related_name="%(class)ss")
    name = models.CharField(max_length=20)
    PRISM_CHOICES = (
        (1, 'Miniprisma'),
        (7, 'Miniprisma 360'),
    )
    prism = models.PositiveSmallIntegerField(choices=PRISM_CHOICES,
                                             default=1)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % self.name


class FipoTarget(TachyTarget):
    use_plane = models.BooleanField(default=True)
    use_height = models.BooleanField(default=True)


class SupoTarget(TachyTarget):
    pass


class TachyTask(models.Model):
    position = models.ForeignKey(TachyPosition, related_name="%(class)ss")
    active = models.BooleanField(default=True)
    from_time = models.TimeField(default=datetime.time(0, 0, 0))
    to_time = models.TimeField(default=datetime.time(23, 59, 59))
    frequency = models.FloatField(default=60.0)

    class Meta:
        abstract = True


class FipoTask(TachyTask):
    target = models.ForeignKey(FipoTarget, related_name="%(class)ss")

    def __unicode__(self):
        return "%s -> %s, %.2f Minuten" % (self.position, self.target)


class SupoTask(TachyTask):
    target = models.ForeignKey(SupoTarget, related_name="%(class)ss")

    def __unicode__(self):
        return "%s -> %s, %.2f Minuten" % (self.position, self.target)


class TachyMeasurement(models.Model):
    horizontal_angle = models.FloatField()
    vertical_angle = models.FloatField()
    slope_distance = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    station = models.ForeignKey(TachyStation, related_name="%(class)ss")
    FACE_ONE = 0
    FACE_TWO = 1
    FACE_CHOICES = (
        (FACE_ONE, 'Lage I'),
        (FACE_TWO, 'Lage II'),
    )
    face = models.PositiveSmallIntegerField(choices=FACE_CHOICES,
                                            default=FACE_ONE)

    class Meta:
        abstract = True


class FipoMeasurement(TachyMeasurement):
    target = models.ForeignKey(FipoTarget, related_name="%(class)ss")

    def __unicode__(self):
        return "%s - %s" % (self.station, self.target)


class SupoMeasurement(TachyMeasurement):
    target = models.ForeignKey(SupoTarget, related_name="%(class)ss")

    def __unicode__(self):
        return "%s - %s" % (self.station, self.target)

    
    
