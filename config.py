"""Configuration options and environment variables."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from decouple import config


DEBUG = config('DEBUG', cast=bool, default=True)
PORT = config('PORT', cast=int, default=5000)

TEMPLATES_AUTO_RELOAD = config('TEMPLATES_AUTO_RELOAD', cast=bool, default=True)

# MONGODB_SETTINGS
MONGODB_DB = config('MONGODB_DB')
MONGODB_HOST = config('MONGODB_HOST')
MONGODB_PORT = config('MONGODB_PORT', cast=int, default=27017)
MONGODB_USERNAME = config('MONGODB_USERNAME')
MONGODB_PASSWORD = config('MONGODB_PASSWORD')
# Flask mongoengine makes uri from the DB name, host, and port
