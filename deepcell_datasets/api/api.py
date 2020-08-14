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
"""Flask blueprint for API."""

from werkzeug.exceptions import HTTPException
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from flask import current_app
from flask import render_template
from flask import url_for, redirect

from flask_login import current_user
from flask_security import login_required
from flask_mongoengine.wtf import model_form

from mongoengine import ValidationError

from deepcell_datasets.database.models import Experiments
from deepcell_datasets.database.models import Samples

from deepcell_datasets.samples.samples import samples_bp

from deepcell_datasets.utils.misc_utils import nest_dict


api_bp = Blueprint('api_bp', __name__,  # pylint: disable=C0103
                   template_folder='templates')


@api_bp.errorhandler(Exception)
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
@api_bp.route('/experiments')
def get_experiments():  # def get_experiments(page=1):
    # paginated_experiments = experiments.objects.paginate(page=page, per_page=10)
    experiments = Experiments.objects().to_json()
    return Response(experiments, mimetype='application/json')


@api_bp.route('/experiments', methods=['POST'])
def create_experiment():
    """Create a new experiments"""
    body = request.get_json()
    current_app.logger.info('Body is %s ', body)
    experiment = Experiments(**body).save()
    current_app.logger.info('experiment %s saved succesfully', experiment)
    unique_id = experiment.id
    current_app.logger.info('unique_id %s extracted as key', unique_id)
    return jsonify({'unique_id': str(unique_id)})


@api_bp.route('/<experiment_id>', methods=['PUT'])
def update_experiment(experiment_id):
    body = request.get_json()
    Experiments.objects.get_or_404(id=experiment_id).update(**body)
    return jsonify({}), 204  # successful update but no content


@api_bp.route('/<experiment_id>', methods=['DELETE'])
def delete_experiment(experiment_id):
    Experiments.objects.get_or_404(id=experiment_id).delete()
    return jsonify({}), 204  # successful update but no content


@api_bp.route('/<experiment_id>')
def get_experiment(experiment_id):
    experiment = Experiments.objects.get_or_404(id=experiment_id).to_json()
    return Response(experiment, mimetype='application/json')


# Sample Routes
@api_bp.route('/samples')
def get_samples():  # def get_samples(page=1):
    # paginated_samples = Samples.objects.paginate(page=page, per_page=10)
    samples = Samples.objects().to_json()
    return Response(samples, mimetype='application/json')


@api_bp.route('/samples', methods=['POST'])
def create_sample():
    """Create a new experiments"""
    body = request.get_json()
    current_app.logger.info('Body is %s ', body)
    sample = Samples(**body).save()
    current_app.logger.info('sample %s saved succesfully', sample)
    unique_id = sample.id
    current_app.logger.info('unique_id %s extracted as key', unique_id)
    return jsonify({'unique_id': str(unique_id)})


# TODO: This shouldnt stay '/' should have a prefix
@api_bp.route('/<sample_id>', methods=['PUT'])
def update_sample(sample_id):
    body = request.get_json()
    Samples.objects.get_or_404(id=sample_id).update(**body)
    return jsonify({}), 204  # successful update but no content


@api_bp.route('/<sample_id>', methods=['DELETE'])
def delete_sample(sample_id):
    Samples.objects.get_or_404(id=sample_id).delete()
    return jsonify({}), 204  # successful update but no content


@api_bp.route('/<sample_id>')
def get_sample(sample_id):
    sample = Samples.objects.get_or_404(id=sample_id).to_json()
    return Response(sample, mimetype='application/json')
