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
"""DeepCell Datasets Module"""

from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension

from deepcell_datasets import config
from deepcell_datasets import database
from deepcell_datasets.general import general
from deepcell_datasets.specimen import specimen


class ReverseProxied(object):
    """Reverse proxy for serving static files over https"""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def create_app():
    """Factory to create the Flask application"""
    app = Flask(__name__)

    app.config.from_object(config)

    app.wsgi_app = ReverseProxied(app.wsgi_app)

    app.jinja_env.auto_reload = True

    database.db.initialize_db(app)

    app.register_blueprint(general.general_bp, url_prefix='/')
    app.register_blueprint(specimen.specimen_bp, url_prefix='/specimen')

    # toolbar = DebugToolbarExtension(app)

    return app