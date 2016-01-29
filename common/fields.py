from common.utils.generate import generate_id
from django.db import models


class IdField(models.Field):
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
        super(IdField, self).__init__(*args, **kwargs)
