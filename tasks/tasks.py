import logging

from dimosy.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def schedule(self):
    logger.debug("Execute schedule task...")
