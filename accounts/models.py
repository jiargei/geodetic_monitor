from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager

from libs import constants

# Create your models here.


class User(AbstractUser):

    objects = UserManager()


class Membership(models.Model):
    """
    Membership controls the user role inside a project.

    An user can work with different roles in different projects but has to be unique for each project.

    fields
    ------

    user: Select user to set role in project for
    project: ...
    role: ...

    """
    user = models.OneToOneField("accounts.User", unique=True)
    project = models.ForeignKey("accounts.Project", on_delete=models.CASCADE)
    role = models.CharField(max_length=1,
                            choices=constants.USER_ROLE_CHOICES,
                            default="u")

    def __unicode__(self):
        return u"%s ist %s in %s" % (self.user,
                                     dict(constants.USER_ROLE_CHOICES).get(self.role),
                                     self.project)


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    token = models.CharField(max_length=10, default='', unique=True)
    active = models.BooleanField(default=True)
    members = models.ManyToManyField(User, through=Membership)

    def __unicode__(self):
        return u"%s - %s" % (self.token, self.name)

    class Meta:
        ordering = ["active", "name"]  # Project.Meta.ordering = []


class Box(models.Model):
    name = models.CharField(max_length=15)
    url = models.URLField()
    project = models.ForeignKey("accounts.Project", blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.project)  # b1 = Box(name="Cygnus"); print b1 -> "Cygnus (BEAX)"

    class Meta:
        verbose_name_plural = "boxes"


class Sensor(models.Model):
    sensor_name = models.CharField(max_length=100)
    sensor_serial = models.CharField(max_length=20, unique=True)
    sensor_type = models.PositiveSmallIntegerField(default=1, choices=constants.SENSOR_TYPE_CHOICES)

    def __unicode__(self):
        return u"%s-%s" % (dict(constants.SENSOR_TYPE_CHOICES).get(self.sensor_type), self.sensor_name)
