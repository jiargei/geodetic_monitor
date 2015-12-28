from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from libs import constants

# Create your models here.


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username, first_name, last_name']


class Membership(models.Model):
    user = models.OneToOneField(CustomUser, unique=True)
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
    members = models.ManyToManyField(CustomUser, through=Membership)

    def __unicode__(self):
        return u"%s - %s" % (self.token, self.name)

    class Meta:
        ordering = ["active", "name"]


class Box(models.Model):
    name = models.CharField(max_length=15)
    url = models.URLField()
    project = models.ForeignKey("accounts.Project", blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.project)

    class Meta:
        verbose_name_plural = "Boxes"


class Sensor(models.Model):
    sensor_name = models.CharField(max_length=100)
    sensor_serial = models.CharField(max_length=20, unique=True)
    sensor_type = models.PositiveSmallIntegerField(default=1, choices=constants.SENSOR_TYPE_CHOICES)

    def __unicode__(self):
        return u"%s-%s" % (dict(constants.SENSOR_TYPE_CHOICES).get(self.sensor_type), self.sensor_name)
