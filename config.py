"""Configuration options and environment variables."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import decouple


DEBUG = decouple.config('DEBUG', cast=bool, default=True)
PORT = decouple.config('PORT', cast=int, default=5000)

TEMPLATES_AUTO_RELOAD = decouple.config('TEMPLATES_AUTO_RELOAD', cast=bool, default=True)

# MONGODB_SETTINGS
MONGODB_SETTINGS = {
	'DB' : decouple.config('MONGODB_DB'),
	'HOST' : decouple.config('MONGODB_HOST'),
	'PORT' : decouple.config('MONGODB_PORT', cast=int, default=27017),
	'USERNAME' : decouple.config('MONGODB_USERNAME'),
	'PASSWORD' : decouple.config('MONGODB_PASSWORD')
}



#MONGODB_DB = decouple.config('MONGODB_DB', cast=str, default='test')
# MONGODB_HOST = config('MONGODB_HOST')
# MONGODB_PORT = config('MONGODB_PORT', cast=int, default=27017)
# MONGODB_USERNAME = config('MONGODB_USERNAME')
# MONGODB_PASSWORD = config('MONGODB_PASSWORD')
# Flask mongoengine makes uri from the DB name, host, and port
