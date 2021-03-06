"""
Django settings for dimosy4 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sg(^0!@l%8b%=x93yqmq3ekiqynf0hyi30264ro+10h7%db2^u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# Django Basic Apps
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# Django Extensions
INSTALLED_APPS += (
    'django_extensions',
    'bootstrap3',
    'polymorphic',
    'django.contrib.contenttypes',
    'import_export',
)

# Dimosy Apps
INSTALLED_APPS += (
    'accounts',
    'alarms',
    'metering',
    'jobs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'jobs': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

ROOT_URLCONF = 'dimosy.urls'

WSGI_APPLICATION = 'dimosy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dimosy',
        'USER': 'dimosy',
        'HOST': 'localhost',
        'DATABASE': 'dimosy',
        'PASSWORD': 'dimosy',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/var/www/dimosy.com/static/"


# rest_framework Settings
# http://www.django-rest-framework.org/api-guide/settings

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]


LOGIN_REDIRECT_URL = 'project-list'

ROLLBAR = {
    'access_token': '4b848a2edb694790923a1c8146a24b8f',
    'environment': 'development' if DEBUG else 'production',
    'root': BASE_DIR,
}
# rollbar.init(**ROLLBAR)

SENSORS = (
    'sensors.tachy.fake.fake_tachy.FakeTachy',
    'sensors.tachy.leica.leica_tachy_tps1100.TPS1100',
    'sensors.tachy.leica.leica_tachy_ts15.TS15',
    'sensors.tachy.leica.leica_tachy_tm30.TM30',
)
BOX_ID = None

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'schedule-jobs': {
        'task': 'jobs.tasks.schedule',
        'schedule': timedelta(seconds=5),
    },
}
