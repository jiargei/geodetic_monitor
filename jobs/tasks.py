import logging
import json

from django.utils import timezone

from dimosy.celery import app
from .models import PeriodicTask
from metering.tasks import meter_task

logger = logging.getLogger(__name__)


@app.task(bind=True)
def schedule(self):

    logger.debug("Execute schedule task...")
    # TODO add some filtering and check is_due
    tasks = PeriodicTask.objects.filter(active=True)
    logger.debug("Checking %s jobs...", len(tasks))
    for task in tasks:
        if task.is_due():

            tmd = {
                "task_id": task.id,
                "object_id": task.object_id,
                "content_type": task.content_type,
                "project": task.project.id,
                "info": str(task)
            }
            tmp_file = "/tmp/dimosy/elk/log/task_%s.log" % timezone.localtime(timezone.now()).strftime("%Y%m%d")
            f = open(tmp_file, 'a')
            f.write(b=json.dumps(tmd))
            f.close()

            logger.debug("Applying task %s...", task)
            meter_task.apply_async([task.id])
