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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import distutils
import json
import os
import re

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import current_app

from database.models import Specimen_Type


bp = Blueprint('deepcell-datasets', __name__)  # pylint: disable=C0103


@bp.route('/health')
def health():
    '''Returns success if the application is ready.'''
    return jsonify({'message': 'success'})


@bp.route('/', methods=['GET', 'POST'])
def form():
    '''Request HTML landing page to be rendered.'''
    return render_template('index.html')


@bp.route('/all_specimen')
def get_all_specimen():
    all_specimen = Specimen_Type.objects().to_json()
    return Response(all_specimen, mimetype="application/json", status=200)


@bp.route('/all_specimen', methods=['POST'])
    body = request.get_json()
    specimen = Specimen_Type(**body).save()
    name = specimen.name
    return {'name': str(name)}, 200


@bp.route('/all_specimen/<name>', methods=['PUT'])
def update_specimen(name):
    body = request.get_json()
    Specimen_Type.objects.get(name=name).update(**body)
    return '', 200


@app.route('/all_specimen/<name>', methods=['DELETE'])
def delete_specimen(name):
    Specimen_Type.objects.get(name=name).delete()
    return '', 200


@app.route('/all_specimen/<name>')
def get_specimen(name):
    all_specimen = Specimen_Type.objects.get(name=name).to_json()
    return Response(all_specimen, mimetype="application/json", status=200)
