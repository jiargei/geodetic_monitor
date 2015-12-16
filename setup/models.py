import datetime
from django.contrib.auth.models import User
from django.db import models

from bitfield import BitField

from lib import CONSTANTS


# Create your models here.


class Membership(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    role = models.CharField(max_length=1,
                            choices=CONSTANTS.USER_ROLE_CHOICES,
                            default="u")

    def __unicode__(self):
        return "%s ist %s in %s" % (self.user,
                                    dict(CONSTANTS.USER_ROLE_CHOICES).get(self.role),
                                    self.project)


class Coordinate(models.Model):
    easting = models.FloatField()
    northing = models.FloatField()
    height = models.FloatField()

    class Meta:
        abstract = True


class TimeWindow(models.Model):
    von = models.TimeField()
    bis = models.TimeField()
    frequency = models.DecimalField(default=10., decimal_places=2, max_digits=5)
    #day_of_week = models.CharField(max_length=7, default="1234567")

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
        find_days = "["
        for dow in self.day_of_week:
            if "1" in dow:
                find_days += "mo,"
            elif "2" in dow:
                find_days += "di,"
            elif "3" in dow:
                find_days += "mi,"
            elif "4" in dow:
                find_days += "do,"
            elif "5" in dow:
                find_days += "fr,"
            elif "6" in dow:
                find_days += "sa,"
            elif "7" in dow:
                find_days += "so,"
        find_days += "]"
        return "%s - %s an %s, %s min" % (self.von, self.bis, self.day_of_week, self.frequency)


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    token = models.CharField(max_length=10, default='')
    active = models.BooleanField(default=True)
    members = models.ManyToManyField(User, through=Membership)

    def __unicode__(self):
        return "%s - %s" % (self.token, self.name)

    class Meta:
        ordering = ["active", "name"]


class Position(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    recent_sensor = models.ForeignKey("Sensor", blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return "%s" % self.name


class Station(Coordinate):
    name = models.CharField(max_length=30)
    position = models.ForeignKey("Position", on_delete=models.CASCADE)
    sensor = models.ForeignKey("Sensor", on_delete=models.SET_NULL, null=True, blank=True)
    von = models.DateTimeField(default=datetime.datetime.now())
    bis = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.position.name)

    class Meta:
        ordering = ["position", "von"]


class Sensor(models.Model):
    name = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.serial_number)


class Target(Coordinate):
    name = models.CharField(max_length=20)
    target_type = models.CharField(default='d', max_length=1, choices=CONSTANTS.TARGET_TYPE_CHOICES)
    prism_type = models.PositiveSmallIntegerField(choices=CONSTANTS.PRISM_CHOICES, default=1)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s (%s)" % (self.name, dict(CONSTANTS.TARGET_TYPE_CHOICES).get(self.target_type))

    class Meta:
        ordering = ["target_type", "name"]


class Task(models.Model):
    time_windows = models.ManyToManyField("TimeWindow")
    position = models.ForeignKey("Position")
    targets = models.ManyToManyField("Target")
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s, %s, %s" % (self.position, self.targets, self.time_windows)

    class Meta:
        ordering = ["position"]


class Box(models.Model):
    name = models.CharField(max_length=15)
    url = models.URLField()
    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.project)


class ObservationType(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    scale = models.FloatField(default=1)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.unit)


class AlarmPlan(models.Model):
    name = models.CharField(max_length=50)
    observation_type = models.ForeignKey(ObservationType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.observation_type)


class AlarmPhase(models.Model):
    alarm_plan = models.ForeignKey(AlarmPlan, on_delete=models.CASCADE)
    state = models.SmallIntegerField(default=0, choices=CONSTANTS.ALARM_STATES)
    value = models.FloatField()

    def __unicode__(self):
        return "%s, %s, %s" % (self.alarm_plan, dict(CONSTANTS.ALARM_STATES).get(self.state), self.value)

    class Meta:
        ordering = ["alarm_plan", "state"]


class AlarmNotification(models.Model):
    alarm_phase = models.ForeignKey(AlarmPhase, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    boxes = models.ManyToManyField(Box)

    by_mail = models.BooleanField(default=True)
    by_text = models.BooleanField(default=True)
    by_light = models.BooleanField(default=True)


class UserNotification(models.Model):
    alarm_phase = models.ForeignKey(AlarmPhase, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    notification_type = BitField(
        flags=(
            'SMS',
            'EMail',
        )
    )


class BoxNotification(models.Model):
    alarm_phase = models.ForeignKey(AlarmPhase, on_delete=models.CASCADE)
    boxes = models.ManyToManyField(Box)
    notification_type = BitField(
        flags=(
            'Blinklicht',
        )
    )
