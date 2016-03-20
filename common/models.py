from django.db import models


class CreatedModifiedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserCreatedMixin(CreatedModifiedMixin):
    creator = models.ForeignKey('accounts.User')

    class Meta:
        abstract = True
