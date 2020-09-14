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
"""Flask blueprint for Experiments data API."""

from werkzeug.exceptions import HTTPException
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from flask import current_app

from mongoengine import ValidationError

from deepcell_datasets.database.models import Training_Data


training_api_bp = Blueprint('training_api_bp', __name__,  # pylint: disable=C0103
                            template_folder='templates')


@training_api_bp.errorhandler(Exception)
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


# TrainingData Routes
@training_api_bp.route('/')
def get_all_training_data():
    training_data = TrainingData.objects().to_json()
    return Response(training_data, mimetype='application/json')


@training_api_bp.route('/<training_data_id>')
def get_training_data(training_data_id):
    training_data = TrainingData.objects.get_or_404(id=training_data_id).to_json()
    return Response(training_data, mimetype='application/json')


# @training_api_bp.route('/', methods=['POST'])
# def create_training_data():
#     """Create a new training data"""
#     body = request.get_json()
#     current_app.logger.info('Body is %s ', body)
#     training_data = TrainingData(**body).save()
#     current_app.logger.info('training_data %s saved succesfully', training_data)
#     unique_id = training_data.id
#     current_app.logger.info('unique_id %s extracted as key', unique_id)
#     return jsonify({'unique_id': str(unique_id)})


# @training_api_bp.route('/<training_data_id>', methods=['PUT'])
# def update_training_data(training_data_id):
#     body = request.get_json()
#     TrainingData.objects.get_or_404(id=training_data_id).update(**body)
#     return jsonify({}), 204  # successful update but no content


# @training_api_bp.route('/<training_data_id>', methods=['DELETE'])
# def delete_training_data(training_data_id):
#     TrainingData.objects.get_or_404(id=training_data_id).delete()
#     return jsonify({}), 204  # successful update but no content
