import logging

from dimosy.celery import app
import serial
import json

from .models import Reference, Position
from sensors import tachy
from geodetic.calculations import polar
from geodetic.point import Point
from common.utils.generate import generate_datestring
logger = logging.getLogger(__name__)


@app.task(bind=True)
def meter_task(self, reference_id):

    tmp_file = "/vagrant/elk/tmp/log/tachy_20160814.log"

    reference = Reference.objects.get(pk=reference_id)

    station = reference.position.stations.latest()
    station_p = Point()
    station_p.set_coordinate(reference.position.stations.latest())
    target_p = Point()
    target_p.set_coordinate(reference.target)

    folding_square = polar.grid_to_polar(station_p, target_p)
    sensor_db = reference.position.stations.latest().sensor
    dev_port = sensor_db.connection.port
    sensor_class = sensor_db.get_sensor_class()
    sensor_real = None
    sensor_serial = serial.Serial(port=dev_port, timeout=5)

    if sensor_class == "TPS1100":
        sensor_real = tachy.leica.leica_tachy_tps1100.TPS1100

    elif sensor_class == "TS15":
        sensor_real = tachy.leica.leica_tachy_ts15.TS15

    assert sensor_real is not None

    sensor_real(serial=sensor_serial)
    sensor_real.set_angles(hz=folding_square["azimut"],
                           v=folding_square["zenit"])

    tm = sensor_real.get_measurement()
    tc = sensor_real.get_target()

    tmd = {"tachy_measurement":
               {
                   "tc": generate_datestring(),
                   "hz": tm["HORIZONTAL_ANGLE"],
                   "v": tm["VERTICAL_ANGLE"],
                   "sd": tm["SLOPE_DISTANCE"],
                   "target": reference.target.name,
                   "station": reference.position.name,
                   "target_easting": tc["EASTING"],
                   "target_northing": tc["NORTHING"],
                   "target_height": tc["HEIGHT"],
                   "station_easting": station.easting,
                   "station_northing": station.northing,
                   "station_height": station.height,
               }
           }

    f = open(tmp_file, 'a')
    f.write(b=json.dumps(tmd))
    f.close()




