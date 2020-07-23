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
"""Flask blueprint for modular routes."""

from flask import Blueprint
from flask import jsonify
from flask import render_template

from flask_security import auth_required, roles_required


general_bp = Blueprint('general_bp', __name__,  # pylint: disable=C0103
                       template_folder='templates')


@general_bp.route('/health')
def health():
    """Returns success if the application is ready."""
    return jsonify({'message': 'success'})


@general_bp.route('/secure')
@auth_required()
def secure():
    """Returns success if the application is ready."""
    return jsonify({'message': 'success'})


@general_bp.route('/admin')
@roles_required('admin')
def admin():
    """Returns success if the application is ready."""
    return jsonify({'message': 'success'})


# TODO: Web interface for wet lab
@general_bp.route('/', methods=['GET'])
def index():
    """Request HTML landing page to be rendered."""
    return render_template('general/index.html')
