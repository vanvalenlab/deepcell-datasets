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
from flask import request
from flask import Response

from deepcell_datasets.database.models import Specimen


specimen_bp = Blueprint('specimen_bp', __name__)  # pylint: disable=C0103


@specimen_bp.route('/')
def get_all_specimen():  # def get_all_specimen(page=1):
    # paginated_all_specimen = Specimen.objects.paginate(page=page, per_page=10)
    try:
        all_specimen = Specimen.objects().to_json()
        return Response(all_specimen, mimetype="application/json")
    except Exception as err:  # TODO: pick the type of exception.
        # Bad request as request object is not available
        return jsonify({'error': str(err)}), 400


@specimen_bp.route('/', methods=['POST'])
def create_specimen():
    """Create a new specimen"""
    # Parse the request
    try:
        body = request.get_json()
    except Exception as err:  # TODO: pick the type of exception.
        # Bad request as request body is not available
        return jsonify({'error': str(err)}), 400

    try:
        specimen = Specimen(**body).save()
        exp_id = specimen.exp_id
        return jsonify({'exp_id': str(exp_id)})
    except Exception as err:  # TODO: pick the type of exception.
        # Error while trying to create resource
        return jsonify({'error': str(err)}), 500


@specimen_bp.route('/<exp_id>', methods=['PUT'])
def update_specimen(exp_id):
    try:
        body = request.get_json()
        Specimen.objects.get(exp_id=exp_id).update(**body)
        return jsonify({})
    except Exception as err:  # TODO: pick the type of exception.
        # Error while trying to update resource
        return jsonify({'error': str(err)}), 500


@specimen_bp.route('/<exp_id>', methods=['DELETE'])
def delete_specimen(exp_id):
    try:
        specimen = Specimen.objects.get(exp_id=exp_id).delete()
        return jsonify({})
    except Exception as err:  # TODO: pick the type of exception.
        # Error while trying to delete resource
        return jsonify({'error': str(err)}), 500


@specimen_bp.route('/<exp_id>')
def get_specimen(exp_id):
    try:
        all_specimen = Specimen.objects.get_or_404(exp_id=exp_id).to_json()
        return Response(all_specimen, mimetype="application/json")
    except Exception as err:  # TODO: pick the type of exception.
        # Bad Request
        return jsonify({'error': str(err)}), 500
