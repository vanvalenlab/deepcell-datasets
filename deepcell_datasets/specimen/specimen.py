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
from flask import request
from flask import Response
from flask import current_app
from werkzeug.exceptions import HTTPException

from deepcell_datasets.database.models import Specimen


specimen_bp = Blueprint('specimen_bp', __name__)  # pylint: disable=C0103


@specimen_bp.errorhandler(Exception)
def handle_exception(err):
    """Error handler

    https://flask.palletsprojects.com/en/1.1.x/errorhandling/
    """
    # pass through HTTP errors
    if isinstance(err, HTTPException):
        return err
    # now you're handling non-HTTP exceptions only
    return jsonify({'error': str(err)}), 500


@specimen_bp.route('/')
def get_all_specimen():  # def get_all_specimen(page=1):
    # paginated_all_specimen = Specimen.objects.paginate(page=page, per_page=10)
    all_specimen = Specimen.objects().to_json()
    return Response(all_specimen, mimetype='application/json')


@specimen_bp.route('/', methods=['POST'])
def create_specimen():
    """Create a new specimen"""
    body = request.get_json()
    current_app.logger.info('Body is %s ', body)
    specimen = Specimen(**body).save()
    current_app.logger.info('Specimen %s saved succesfully', specimen)
    unique_id = specimen.id
    current_app.logger.info('unique_id %s extracted as key', unique_id)
    return jsonify({'unique_id': str(unique_id)})


@specimen_bp.route('/<specimen_id>', methods=['PUT'])
def update_specimen(specimen_id):
    body = request.get_json()
    Specimen.objects.get_or_404(id=specimen_id).update(**body)
    return jsonify({}), 204  # successful update but no content


@specimen_bp.route('/<specimen_id>', methods=['DELETE'])
def delete_specimen(specimen_id):
    specimen = Specimen.objects.get_or_404(id=specimen_id).delete()
    return jsonify({}), 204  # successful update but no content


@specimen_bp.route('/<specimen_id>')
def get_specimen(specimen_id):
    specimen = Specimen.objects.get_or_404(id=specimen_id).to_json()
    return Response(specimen, mimetype='application/json')
