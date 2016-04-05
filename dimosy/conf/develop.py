from base import *

INSTALLED_APPS += ('kombu.transport.django', )
BROKER_URL = "django://"
