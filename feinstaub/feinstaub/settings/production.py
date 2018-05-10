#
# TODOs
#
# rename this file to production.py
#
import os

from .base import *

DEBUG = True

# add your host here:
ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/home/uid1000/feinstaub/static/'


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


USE_X_FORWARDED_HOST = True

# set a new secret key:
SECRET_KEY = os.getenv("API_SECRET_KEY", "FIXME")

# set some secrets for APIs
FORECAST_IO_KEY = os.getenv("API_FORECAST_IO_KEY", "FIXME")
