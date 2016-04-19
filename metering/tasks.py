import logging

from dimosy.celery import app
import serial
import json

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from .models import Reference, Position
from tasks.models import PeriodicTask
from sensors import tachy
from geodetic.calculations import polar
from geodetic.point import Point
from common.utils.generate import generate_datestring
logger = logging.getLogger(__name__)


@app.task(bind=True)
def meter_task(self, task_id):

    tmp_file = "/vagrant/elk/tmp/log/tachy_%s.log" % timezone.now().strftime("%Y%m%d")

    reference_id = task_id
    reference = None

    task = PeriodicTask.objects.get(pk=task_id)
    reference = task.task_object

    assert isinstance(reference, Reference)

    station = reference.position.stations.latest()
    station_p = Point()
    station_p.set_coordinate(station)
    target_p = Point()
    target_p.set_coordinate(reference.target)

    folding_square = polar.grid_to_polar(station_p, target_p)
    sensor_db = station.sensor
    dev_port = sensor_db.connection.port

    sensor_class = sensor_db.get_sensor_class()
    sensor_serial = serial.Serial(port=dev_port, timeout=5)

    assert sensor_class is not None

    sensor_class(serial=sensor_serial)
    sensor_class.set_angles(hz=folding_square["azimut"],
                           v=folding_square["zenit"])

    tm = sensor_class.get_measurement()
    tl = sensor_class.get_compensator()
    tt = sensor_class.get_temperature()
    tc = sensor_class.get_target()
    profiles = []
    # for profile in reference.target.profiles:
    #     pass

    tmd = {
        "id": tm["UID"],
        "created": timezone.now(),
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
            "id": reference.position.pk,
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
            "device_temperature": tt,
            "reflector_height": 0.0,  # TODO
           },
        "obtained": {
            "deasting": tm["EASTING"] - reference.target.easting,
            "dnorthing": tm["NORTHING"] - reference.target.northing,
            "dheight": tm["HEIGHT"] - reference.target.height,
            "slope_distance_reduced": tm["SLOPE_DISTANCE"],  # TODO ..
            "profiles": profiles,
        },
    }

    f = open(tmp_file, 'a')
    f.write(b=json.dumps(tmd, cls=DjangoJSONEncoder))
    f.close()




