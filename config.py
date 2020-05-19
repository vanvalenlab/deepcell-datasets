"""Configuration options and environment variables."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from decouple import config


DEBUG = config('DEBUG', cast=bool, default=True)
PORT = config('PORT', cast=int, default=5000)

TEMPLATES_AUTO_RELOAD = config('TEMPLATES_AUTO_RELOAD', cast=bool, default=True)

# MONGODB_SETTINGS
MONGODB_DB = config('DC_Datasets')
MONGODB_HOST = config('localhost')
MONGODB_PORT = config(27017)
MONGODB_USERNAME = config('webapp')
MONGODB_PASSWORD = config('pwd123')
# Flask mongoengine makes uri from the DB name, host, and port
