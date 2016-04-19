from common.utils.generate import generate_id
from django.db import models
from django.db.models import Lookup
from django.db.models.fields import Field


class UIDField(models.CharField):
    """
    Creates Id

    :return: Random Id
    :rtype: str
    """

    description = "Generates a random Id"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        kwargs['unique'] = True
        kwargs['primary_key'] = True
        kwargs['default'] = generate_id
        kwargs['db_index'] = True
        kwargs['editable'] = False
        super(UIDField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        # newer Django versions need this method to be able to construct
        # migrations correctly
        # https://docs.djangoproject.com/en/1.9/howto/custom-model-fields/#field-deconstruction
        name, path, args, kwargs = super(UIDField, self).deconstruct()
        for kwarg in ('max_length', 'unique', 'primary_key',
                      'default', 'db_index', 'editable'):
            del kwargs[kwarg]
        return name, path, args, kwargs


@Field.register_lookup
class ContentTypeLookup(Lookup):
    lookup_name = "ct"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = compiler.compile(self.lhs.lhs)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 


# @Field.register_lookup
# class DatetimeLookup(Lookup):
#
#     lookup_name = "dt"
#
#     def as_sql(self, compiler, connection):
#         lhs, lhs_params = compiler.compile(self.lhs.lhs)
#         rhs, rhs_params = self.process_rhs(compiler, connection)
#         params = lhs_params + rhs_params + lhs_params + rhs_params
#         return '%s < %s AND %s > -%s' % (lhs, rhs, lhs, rhs), params