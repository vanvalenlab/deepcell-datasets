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
"""Flask blueprint for Annotations data API."""

from werkzeug.exceptions import HTTPException
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from flask import current_app

from mongoengine import ValidationError

from deepcell_datasets.database.models import Annotations


annotations_api_bp = Blueprint('annotations_api_bp', __name__,  # pylint: disable=C0103
                               template_folder='templates')


@annotations_api_bp.errorhandler(Exception)
def handle_exception(err):
    """Error handler

    https://flask.palletsprojects.com/en/1.1.x/errorhandling/
    """
    # pass through HTTP errors
    if isinstance(err, HTTPException):
        return err
    elif isinstance(err, ValidationError):
        return jsonify({'error': str(err)}), 400
    # now you're handling non-HTTP exceptions only
    current_app.logger.error('Encountered unexpected %s: %s.',
                             err.__class__.__name__, err)
    return jsonify({'error': str(err)}), 500


# Experiment Routes
@annotations_api_bp.route('/')
def get_annotations():  # def get_annotations(page=1):
    # paginated_annotations = annotations.objects.paginate(page=page, per_page=10)
    annotations = Annotations.objects().to_json()
    return Response(annotations, mimetype='application/json')


# TODO: Implement session/CSRF Tokens for API access
@annotations_api_bp.route('/', methods=['POST'])
def create_annotation():
    """Create a new annotations"""
    body = request.get_json()
    current_app.logger.info('Body is %s ', body)
    annotation = Annotations(**body).save()
    current_app.logger.info('annotation %s saved succesfully', annotation)
    unique_id = annotation.id
    current_app.logger.info('unique_id %s extracted as key', unique_id)
    return jsonify({'unique_id': str(unique_id)})


@annotations_api_bp.route('/<annotation_id>', methods=['PUT'])
def update_annotation(annotation_id):
    body = request.get_json()
    Annotations.objects.get_or_404(id=annotation_id).update(**body)
    return jsonify({}), 204  # successful update but no content


@annotations_api_bp.route('/<annotation_id>', methods=['DELETE'])
def delete_annotation(annotation_id):
    Annotations.objects.get_or_404(id=annotation_id).delete()
    return jsonify({}), 204  # successful update but no content


@annotations_api_bp.route('/<annotation_id>')
def get_annotation(annotation_id):
    annotation = Annotations.objects.get_or_404(id=annotation_id).to_json()
    return Response(annotation, mimetype='application/json')
