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
"""Flask application entrypoint for DeepCell MDM"""

from __future__ import absolute_import, division, print_function

import logging

from flask.logging import default_handler

from deepcell_datasets import config, create_app


def initialize_logger():
    """Set up logger format and level"""
    formatter = logging.Formatter(
        '[%(asctime)s]:[%(levelname)s]:[%(name)s]: %(message)s'
    )

    default_handler.setFormatter(formatter)
    default_handler.setLevel(logging.DEBUG)

    wsgi_handler = logging.StreamHandler(
        stream='ext://flask.logging.wsgi_errors_stream'
    )
    wsgi_handler.setFormatter(formatter)
    wsgi_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(default_handler)

    # 3rd party loggers
    logging.getLogger('botocore').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)


if __name__ == '__main__':
    application = create_app()  # pylint: disable=C0103
    initialize_logger()
    application.run('0.0.0.0', port=config.PORT, debug=config.DEBUG)
