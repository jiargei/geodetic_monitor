from dimosy.celery import app
import serial

from .models import Reference
from .. import sensors


@app.task(bind=True)
def meter_task(self, reference_id):
    reference = Reference.objects.get(pk=reference_id)
    sensor_db = reference.position.stations.latest().sensor
    dev_port = sensor_db.connection.port
    sensor_class = sensor_db.get_sensor_class()
    sensor_real = None
    sensor_serial = serial.Serial(port=dev_port)

    if sensor_class == "TPS1100":
        sensor_real = sensors.tachy.leica.leica_tachy_tps1100.TPS1100

    assert sensor_real is not None

    sensor_real(serial=sensor_serial)
    sensor_real.get_measurement()
