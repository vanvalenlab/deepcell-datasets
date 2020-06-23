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

# DEBUG_TB_PANELS = ['flask_mongoengine.panels.MongoDebugPanel']


#MONGODB_DB = decouple.config('MONGODB_DB', cast=str, default='test')
# MONGODB_HOST = config('MONGODB_HOST')
# MONGODB_PORT = config('MONGODB_PORT', cast=int, default=27017)
# MONGODB_USERNAME = config('MONGODB_USERNAME')
# MONGODB_PASSWORD = config('MONGODB_PASSWORD')
# Flask mongoengine makes uri from the DB name, host, and port
