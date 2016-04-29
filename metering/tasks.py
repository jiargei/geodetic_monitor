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

import uuid
import sensors
logger = logging.getLogger(__name__)


@app.task(bind=True)
def meter_task(self, task_id):
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
    station_p = Point()
    station_p.set_coordinate(station.get_point())
    logger.info("Station: %s" % station_p)
    target_p = Point()
    target_p.set_coordinate(reference.target.get_point())
    logger.info("Target: %s" % target_p)

    folding_square = polar.grid_to_polar(station_p, target_p)

    sensor_class = station.sensor.get_sensor_class()

    assert sensor_class is not None
    logger.info("Sensor on port %s" % station.port)

    if sensor_class.__name__ == "FakeTachy":
        sensor_class = sensor_class(connector=None)
    elif sensor_class.brand == "Leica Geosystems":
        sensor_class = sensor_class(connector=serial.Serial(port=station.port, timeout=5))
    else:
        raise NoSensorError

    sensor_class.set_station(easting=station.easting,
                             northing=station.northing,
                             height=station.height,
                             instrument_height=0.0)

    sensor_class.set_polar(horizontal_angle=folding_square["azimut"],
                           vertical_angle=folding_square["zenit"],
                           aim_target=True)

    tm = sensor_class.get_measurement()
    tl = sensor_class.get_compensator()
    tt = sensor_class.get_temperature()
    tc = sensor_class.get_target()

    profiles = []
    for p in reference.target.profiles.all():
        t0 = p.get_target(reference.target.as_point())
        ti = p.get_target(tc.as_point())

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
    print profiles

    tmd = {
        "tachy_measurement": {
            "id": tm.uuid,
            "created": tm.created,
            "target": {
                "id": reference.target.pk,
                "name": reference.target.name,
                "easting": reference.target.easting,
                "northing": reference.target.northing,
                "height": reference.target.height,
                "reflector_height": 0.0,  # TODO
            },
            "position_id": reference.position.pk,
            "reference_id": reference.pk,
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
            "raw": {
                "horizontal_angle": tm.horizontal_angle,
                "vertical_angle": tm.vertical_angle,
                "slope_distance": tm.slope_distance,
                "easting": tc.easting,
                "northing": tc.northing,
                "height": tc.height,
                "compensator_cross": tl.compensator_cross,
                "compensator_length": tl.compensator_length,
                "device_temperature": tt.temperature,
                "reflector_height": tm.reflector_height,
               },
            "obtained": {
                "deasting": tc.easting - reference.target.easting,
                "dnorthing": tc.northing - reference.target.northing,
                "dheight": tc.height - reference.target.height,
                "slope_distance_reduced": tm.slope_distance_reduced,
                "profiles": profiles,
            },
        }
    }

    sensor_class.set_laser_pointer(0)

    tmp_file = "/vagrant/tmp/log/multi_%s.log" % tmp_time.strftime("%Y%m%d")
    f = open(tmp_file, 'a')
    f.write(str(json.dumps(tmd, cls=DjangoJSONEncoder))+"\n")
    f.close()
    task.id_completed = True
    task.save()





