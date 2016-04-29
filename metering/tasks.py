import logging

from dimosy.celery import app
import serial
import math
import json

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from .models import Reference, Position
from jobs.models import PeriodicTask
import apps
from sensors import tachy
from geodetic.calculations import polar
from geodetic.point import Point
from geodetic.calculations.transformation import Helmert2DTransformation
from common.exceptions import NoSensorError
from elk.elasticsearch.common import utils as es_utils

import uuid
import sensors
logger = logging.getLogger(__name__)


@app.task(bind=True)
def meter_task(self, task_id, group_time):
    """

    :param self:
    :param task_id: ID from PeriodicTask
    :return:
    """
    task = PeriodicTask.objects.get(pk=task_id)
    logger.info("Execute task %s...", task.id)

    tmp_time = timezone.localtime(timezone.now())

    reference = task.task_object
    assert isinstance(reference, Reference)

    station = reference.position.stations.latest()
    sensor_class = station.sensor.get_sensor_class()

    assert sensor_class is not None
    logger.info("Sensor on port %s" % station.port)

    if sensor_class.__name__ == "FakeTachy":
        sensor_class = sensor_class(connector=None)
    elif sensor_class.brand in ["Leica Geosystems"]:
        sensor_class = sensor_class(connector=serial.Serial(port=station.port, timeout=5))
    else:
        raise NoSensorError

    tmd = sensor_class.get_es_data(station=station.as_point(),
                                   target=reference.target.as_point())
    profiles = []

    for p in reference.target.profiles.all():
        t0 = p.get_target(reference.target.as_point())
        ti = p.get_target(Point(tmd["tachy_measurement"]["raw"].easting,
                                tmd["tachy_measurement"]["raw"].northing,
                                tmd["tachy_measurement"]["raw"].height))

        pi = {
            "profile": {
                "name": p.name,
                "system": {
                    "startpoint": {
                        "easting": float(p.p1_easting),
                        "northing": float(p.p1_northing),
                    },
                    "endpoint": {
                        "easting": float(p.p2_easting),
                        "northing": float(p.p2_northing),
                    }
                },
                "target": {
                    "id": reference.target.pk,
                    "name": reference.target.name,
                    "reference": {
                        "easting": float(t0["to"].x),
                        "northing": float(t0["to"].y)
                    },
                    "last": {
                        "easting": float(ti["to"].x),
                        "northing": float(ti["to"].y)
                    },
                    "delta": {
                        "easting": float(ti["to"].x - t0["to"].x),
                        "northing": float(ti["to"].y - t0["to"].y)
                    }
                }
            }
        }
        profiles.append(pi)

    tmd["tachy_measurement"].update({
        "group_time": group_time,
        "position_id": reference.position.pk,
        "project_id": task.project.pk,
        "reference_id": reference.pk,
        "target": {
            "id": reference.target.pk,
            "name": reference.target.name,
            "easting": reference.target.easting,
            "northing": reference.target.northing,
            "height": reference.target.height,
            "reflector_height": 0.0,  # TODO
        },
        "station": {
            "id": station.pk,
            "created": station.from_date,
            "easting": station.easting,
            "northing": station.northing,
            "height": station.height,
        },
        "task": {
            "id": task.pk,
            "type": "periodic",
        },
        "obtained": {
            "deasting": tmd["tachy_measurement"]["raw"].easting - reference.target.easting,
            "dnorthing": tmd["tachy_measurement"]["raw"].northing - reference.target.northing,
            "dheight": tmd["tachy_measurement"]["raw"].height - reference.target.height,
            "slope_distance_reduced": tmd["tachy_measurement"]["raw"].slope_distance_reduced,
            "profiles": profiles,
        },
    })

    tmp_file = "/vagrant/tmp/log/multi_%s.log" % tmp_time.strftime("%Y%m%d")
    f = open(tmp_file, 'a')
    f.write(str(json.dumps(tmd, cls=DjangoJSONEncoder))+"\n")
    f.close()
    task.last_success = tmp_time
    task.save()


@app.task(bind=True)
def resection_task(self, task_id, group_time):
    """

    Args:
        self:
        task_id:
        group_time:

    Returns:

    """

    task = PeriodicTask.objects.get(pk=task_id)
    position = task.task_object
    assert isinstance(position, Position)

    # get grouped fipo measurements due to group_time
    measurements = es_utils.get_measurements(group_time)

    # calculate new station
    new_station = Point()

    tmd = {
        "tachy_restation": {
            "id": str(uuid.uuid1()),
            "group_time": group_time,
            "position_id": position.pk,
            "project_id": task.project.pk,
            "measurements": measurements,
            "station": {
                "easting": new_station.x,
                "northing": new_station.y,
                "height": new_station.z
            },
        }
    }

    tmp_time = timezone.localtime(timezone.now())
    tmp_file = "/vagrant/tmp/log/multi_%s.log" % tmp_time.strftime("%Y%m%d")
    f = open(tmp_file, 'a')
    f.write(str(json.dumps(tmd, cls=DjangoJSONEncoder))+"\n")
    f.close()
