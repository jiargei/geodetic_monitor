from dimosy.celery import app

from .models import Reference

@app.task(bind=True)
def meter_task(self, reference_id):
    reference = Reference.objects.get(pk=reference_id)
    sensor = reference.position.stations.latest().sensor
    sensor_class = sensor.get_sensor_class()

    # TODO gerät ansteuern und messung auslösen
