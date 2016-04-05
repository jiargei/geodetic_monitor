from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

from common import constants
from common.fields import UIDField
from common.models import UserCreatedMixin, CreatedModifiedMixin


class User(AbstractUser):
    """

    """
    # objects = UserManager()
    pass


class Project(UserCreatedMixin, models.Model):
    """

    """
    id = UIDField()
    status = models.PositiveSmallIntegerField(default=constants.STATUS_ACTIVE,
                                              choices=constants.STATUS_CHOICES,
                                              db_index=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    token = models.CharField(max_length=10, default='', unique=True)
    active = models.BooleanField(default=True)
    members = models.ManyToManyField(User, through="accounts.Membership",
                                     related_name='projects')

    class Meta:
        ordering = ["active", "name"]


    def __unicode__(self):
        return u"%s - %s" % (self.token, self.name)

    @models.permalink
    def get_absolute_url(self):
        return 'project-detail', (), {'project_id': self.pk}



class Membership(CreatedModifiedMixin, models.Model):
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
    user = models.ForeignKey(User, related_name='memberships')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='memberships')
    role = models.CharField(max_length=1,
                            choices=constants.USER_ROLE_CHOICES,
                            default="u")

    def __unicode__(self):
        return u"%s ist %s in %s" % (self.user,
                                     dict(constants.USER_ROLE_CHOICES).get(self.role),
                                     self.project)

    class Meta:
        unique_together = [("user", "project")]


class Box(UserCreatedMixin, models.Model):
    """

    """
    id = UIDField()
    status = models.PositiveSmallIntegerField(default=constants.STATUS_ACTIVE,
                                              choices=constants.STATUS_CHOICES,
                                              db_index=True)
    name = models.CharField(max_length=15)
    url = models.URLField()
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.project)  # b1 = Box(name="Cygnus"); print b1 -> "Cygnus (BEAX)"

    class Meta:
        verbose_name_plural = "boxes"
