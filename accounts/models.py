from __future__ import unicode_literals

from common import constants
from common.fields import UIDField
from django.contrib.auth.models import AbstractUser
# from django.apps import User
from django.db import models


# Create your models here.


class User(AbstractUser):
    """

    """
    # objects = UserManager()
    pass


class Project(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    token = models.CharField(max_length=10, default='', unique=True)
    active = models.BooleanField(default=True)
    members = models.ManyToManyField(User, through="accounts.Membership")

    def __unicode__(self):
        return u"%s - %s" % (self.token, self.name)

    class Meta:
        ordering = ["active", "name"]


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
    id = UIDField()
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=1,
                            choices=constants.USER_ROLE_CHOICES,
                            default="u")

    def __unicode__(self):
        return u"%s ist %s in %s" % (self.user,
                                     dict(constants.USER_ROLE_CHOICES).get(self.role),
                                     self.project)

    class Meta:
        unique_together = [("user", "project")]


class Box(models.Model):
    """

    """
    id = UIDField()
    name = models.CharField(max_length=15)
    url = models.URLField()
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.project)  # b1 = Box(name="Cygnus"); print b1 -> "Cygnus (BEAX)"

    class Meta:
        verbose_name_plural = "boxes"
