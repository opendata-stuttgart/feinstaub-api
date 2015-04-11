# coding=utf-8

import os
from .base import *

# ######### TEST SETTINGS
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = SITE_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"


if os.environ.get('TEST_ON_PLATFORM', '').lower() == 'wercker':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.environ.get('WERCKER_POSTGRESQL_HOST', '127.0.01'),
            'NAME': os.environ.get('WERCKER_POSTGRESQL_DATABASE', 'test'),
            'TEST_NAME': os.environ.get('WERCKER_POSTGRESQL_DATABASE', 'test'),
            'USER': os.environ.get('WERCKER_POSTGRESQL_USERNAME', 'postgres'),
            'PASSWORD': os.environ.get('WERCKER_POSTGRESQL_PASSWORD', ''),
            'HOST': os.environ.get('WERCKER_POSTGRESQL_HOST', '127.0.01'),
            'PORT': os.environ.get('WERCKER_POSTGRESQL_PORT', '5432'),
        }
    }
