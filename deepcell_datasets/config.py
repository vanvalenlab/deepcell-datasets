# Copyright 2016-2020 The Van Valen Lab at the California Institute of
# Technology (Caltech), with support from the Paul Allen Family Foundation,
# Google, & National Institutes of Health (NIH) under Grant U24CA224309-01.
# All rights reserved.
#
# Licensed under a modified Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.github.com/vanvalenlab/deepcell-datasets/LICENSE
#
# The Work provided may be used for non-commercial academic purposes only.
# For any other use of the Work, including commercial use, please contact:
# vanvalenlab@gmail.com
#
# Neither the name of Caltech nor the names of its contributors may be used
# to endorse or promote products derived from this software without specific
# prior written permission.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Configuration options and environment variables."""

import decouple


DEBUG = decouple.config('DEBUG', cast=bool, default=True)
PORT = decouple.config('PORT', cast=int, default=5000)

TEMPLATES_AUTO_RELOAD = decouple.config('TEMPLATES_AUTO_RELOAD', cast=bool, default=True)

# Flask-Mail settings: https://tinyurl.com/y3db5s3h
MAIL_SERVER = decouple.config('MAIL_SERVER', default='localhost')
MAIL_PORT = decouple.config('MAIL_PORT', default=587, cast=int)
MAIL_USE_TLS = decouple.config('MAIL_USE_TLS', default=True, cast=bool)
MAIL_USE_SSL = decouple.config('MAIL_USE_SSL', default=False, cast=bool)
MAIL_USERNAME = decouple.config('MAIL_USERNAME', default=None)
MAIL_PASSWORD = decouple.config('MAIL_PASSWORD', default=None)
MAIL_DEFAULT_SENDER = decouple.config('MAIL_DEFAULT_SENDER', default='datasets@mail.deepcell.org')
MAIL_MAX_EMAILS = decouple.config('MAIL_MAX_EMAILS', default=None)

# Flask-Security-Too settings: https://tinyurl.com/y5d2n9ry
# Generate a nice key using secrets.token_urlsafe()
SECRET_KEY = decouple.config('SECRET_KEY', default='super-secret')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
SECURITY_PASSWORD_SALT = decouple.config('SECURITY_PASSWORD_SALT', default='salt')
# Enable new users to create accounts
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = MAIL_SERVER != 'localhost'
# Enable users to reset/recover their password
SECURITY_RECOVERABLE = MAIL_SERVER != 'localhost'
SECURITY_RESET_PASSWORD_WITHIN = '3 days'
# Enable users to change their password
SECURITY_CHANGEABLE = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = MAIL_SERVER != 'localhost'
# Send an confirmation email, but allow login without it
SECURITY_CONFIRMABLE = MAIL_SERVER != 'localhost'
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
# Tracks basic user login statistics
SECURITY_TRACKABLE = True

# TODO: Set to True for faster (non-user-related) dev
LOGIN_DISABLED = False

# TODO: This should be enabled when we move to production
WTF_CSRF_ENABLED = False

ADMIN_EMAIL = decouple.config('ADMIN_EMAIL', default='admin@me.com')
ADMIN_PASSWORD = decouple.config('ADMIN_PASSWORD', default='password')

# flask-mongoengine settings
MONGODB_SETTINGS = {
    'DB': decouple.config('MONGODB_DB', default='test'),
    'HOST': decouple.config('MONGODB_HOST', default='localhost'),
    'PORT': decouple.config('MONGODB_PORT', cast=int, default=27017),
    'USERNAME': decouple.config('MONGODB_USERNAME', default=None),
    'PASSWORD': decouple.config('MONGODB_PASSWORD', default=None)
}

# Explain loading only if in DEBUG mode.
EXPLAIN_TEMPLATE_LOADING = DEBUG

# DEBUG_TB_PANELS = ['flask_mongoengine.panels.MongoDebugPanel']

# Flask mongoengine makes uri from the DB name, host, and port
# MONGODB_DB = decouple.config('MONGODB_DB', cast=str, default='test')
# MONGODB_HOST = decouple.config('MONGODB_HOST', default='localhost')
# MONGODB_PORT = decouple.config('MONGODB_PORT', cast=int, default=27017)
# MONGODB_USERNAME = decouple.config('MONGODB_USERNAME', default=None)
# MONGODB_PASSWORD = decouple.config('MONGODB_PASSWORD', default=None)
