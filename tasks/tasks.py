import logging

from dimosy.celery import app


logger = logging.getLogger(__name__)

from .models import PeriodicTask
from ..metering.tasks import meter_task


@app.task(bind=True)
def schedule(self):
    logger.debug("Execute schedule task...")
    # TODO add some filtering and check is_due
    tasks = PeriodicTask.objects.all()
    logger.debug("Checking %s tasks...", len(tasks))
    for task in tasks:
        if task.is_due():
            logger.debug("Applying task %s...", task)
            meter_task.apply_async([task.id])
