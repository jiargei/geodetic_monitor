import logging
import json

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from dimosy.celery import app
from .models import PeriodicTask
from metering.tasks import meter_task

logger = logging.getLogger(__name__)


@app.task(bind=True)
def schedule(self):
    tmp_time = timezone.localtime(timezone.now())
    logger.debug("Execute schedule task...")
    # TODO add some filtering and check is_due
    tasks = PeriodicTask.objects.filter(active=True)
    logger.debug("Checking %s jobs...", len(tasks))
    for task in tasks:
        if not task.is_due():
            continue
        tmd = {
            "periodic_task": {
                "task_id": task.id,
                "object_id": task.object_id,
                "content_type": task.task_object.__class__.__name__,
                "project": task.project.id,
                "info": str(task)
            }
        }
        tmp_file = "/vagrant/tmp/log/multi_%s.log" % tmp_time.strftime("%Y%m%d")
        f = open(tmp_file, 'a')
        f.write(str(json.dumps(tmd, cls=DjangoJSONEncoder))+"\n")
        f.close()
        # logger.debug("wrote JSON to log file")

        logger.debug("Applying task %s...", task.id)
        task.last_started = tmp_time
        task.save()
        meter_task.apply_async([task.id])
