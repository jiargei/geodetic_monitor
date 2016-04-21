import logging

from dimosy.celery import app
import serial
import json

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from .models import Reference, Position
from jobs.models import PeriodicTask
import apps
from sensors import tachy
from geodetic.calculations import polar
from geodetic.point import Point
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
    logger.info("Station: ", station_p)
    target_p = Point()
    target_p.set_coordinate(reference.target.get_point())
    logger.info("Target: ", target_p)

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
    tm["UID"] = str(uuid.uuid1())
    tl = sensor_class.get_compensator()
    tt = sensor_class.get_temperature()
    tc = sensor_class.get_target()
    profiles = []
    # for profile in reference.target.profiles:
    #     pass

    tmd = {
        "id": tm["UID"],
        "created": tmp_time,
        "target": {
            "id": reference.target.pk,
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
            "horizontal_angle": tm["HORIZONTAL_ANGLE"],
            "vertical_angle": tm["VERTICAL_ANGLE"],
            "slope_distance": tm["SLOPE_DISTANCE"],
            "easting": tc["EASTING"],
            "northing": tc["NORTHING"],
            "height": tc["HEIGHT"],
            "compensator_cross": tl["COMPENSATOR_CROSS"],
            "compensator_length": tl["COMPENSATOR_LENGTH"],
            "device_temperature": tt["TEMPERATURE"],
            "reflector_height": 0.0,  # TODO
           },
        "obtained": {
            "deasting": tc["EASTING"] - reference.target.easting,
            "dnorthing": tc["NORTHING"] - reference.target.northing,
            "dheight": tc["HEIGHT"] - reference.target.height,
            "slope_distance_reduced": tm["SLOPE_DISTANCE"],  # TODO ..
            "profiles": profiles,
        },
    }

    tmp_file = "/vagrant/tmp/log/tachy_%s.log" % tmp_time.strftime("%Y%m%d")
    f = open(tmp_file, 'a')
    f.write(str(json.dumps(tmd, cls=DjangoJSONEncoder))+"\n")
    f.close()





