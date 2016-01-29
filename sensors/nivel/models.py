from __future__ import unicode_literals

from sensors.models import Sensor
from sensors.nivel import constants as nc
from django.db import models

# Create your models here.

class NivelSensor(Sensor):
    sensor_model = models.PositiveSmallIntegerField(choices=nc.MODEL_TYPE_CHOICE, default=11)