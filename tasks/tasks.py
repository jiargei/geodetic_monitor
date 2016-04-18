import logging

from dimosy.celery import app

logger = logging.getLogger(__name__)

from .models import PeriodicTask


@app.task(bind=True)
def schedule(self):
    logger.debug("Execute schedule task...")
    tasks = PeriodicTask.objects.all()
    logger.debug("Checking %s tasks...", len(tasks))
    for task in tasks:
        pass
