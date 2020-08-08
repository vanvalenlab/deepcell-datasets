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
from deepcell_datasets.database.models import Methods


experiments_bp = Blueprint('experiments_bp', __name__,  # pylint: disable=C0103
                           template_folder='templates')


# TODO: It would be better for this to live in a 'forms' module
# Should this exclude created_by as we will add this through current_user
# ExperimentForm = model_form(Experiments, exclude=('created_by'))
# MethodsForm = fields.FormField(Methods)
BaseExperimentForm = model_form(Experiments, exclude=('created_by'))
ExperimentForm = model_form(Methods, BaseExperimentForm)


@experiments_bp.errorhandler(Exception)
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


@experiments_bp.route('/')
def get_experiments():  # def get_experiments(page=1):
    # paginated_experiments = experiments.objects.paginate(page=page, per_page=10)
    experiments = Experiments.objects().to_json()
    return Response(experiments, mimetype='application/json')


@experiments_bp.route('/', methods=['POST'])
def create_experiment():
    """Create a new experiments"""
    body = request.get_json()
    current_app.logger.info('Body is %s ', body)
    experiment = Experiments(**body).save()
    current_app.logger.info('experiment %s saved succesfully', experiment)
    unique_id = experiment.id
    current_app.logger.info('unique_id %s extracted as key', unique_id)
    return jsonify({'unique_id': str(unique_id)})


@experiments_bp.route('/<experiment_id>', methods=['PUT'])
def update_experiment(experiment_id):
    body = request.get_json()
    Experiments.objects.get_or_404(id=experiment_id).update(**body)
    return jsonify({}), 204  # successful update but no content


@experiments_bp.route('/<experiment_id>', methods=['DELETE'])
def delete_experiment(experiment_id):
    Experiments.objects.get_or_404(id=experiment_id).delete()
    return jsonify({}), 204  # successful update but no content


@experiments_bp.route('/<experiment_id>')
def get_experiment(experiment_id):
    experiment = Experiments.objects.get_or_404(id=experiment_id).to_json()
    return Response(experiment, mimetype='application/json')


# Routes for HTML pages.
@experiments_bp.route('/data_entry', methods=['GET', 'POST'])
@login_required
def add_experiment():
    form = ExperimentForm()
    if form.validate_on_submit():
        # Do something with data
        body_raw = request.form
        current_app.logger.info('Form body is %s ', body_raw)

        body_dict = nest_dict(body_raw.to_dict())
        current_app.logger.info('Nested dict to save is %s ', body_dict)
        experiment = Experiments(**body_dict).save()

        current_app.logger.info('experiment %s saved succesfully', experiment)
        unique_id = experiment.id
        current_app.logger.info('unique_id %s extracted as key', unique_id)

        # doi_information = request.form['doi']
        # date_information = request.form['date_collected']
        # imaging_info = request.form
        # subtype_info = request.form['methods-subtype']
        # current_app.logger.info('doi information from form: %s', doi_information)
        # current_app.logger.info('date information from form: %s', date_information)
        # current_app.logger.info('method information from form: %s', imaging_info)
        # current_app.logger.info('method information from form: %s', subtype_info)


        return redirect(url_for('experiments_bp.success'))
    return render_template('experiments/data_entry.html',
                           form=form,
                           current_user=current_user)


@experiments_bp.route('/success')
def success():
    return 'Experiment Successfully Submitted'


# TODO: This should not live here permanently
# Utility functions
def nest_dict(flat_dict, sep='-'):
    """Return nested dict by splitting the keys on a delimiter.

    """

    # Start a new dict to hold top level keys and take values for these top level keys
    new_dict={}
    hyphen_dict={}
    eds = set()
    for k, v in flat_dict.items():
        if '-' not in k:
            new_dict[k] = v
        else:
            hyphen_dict[k] = v
            eds.add(k.split(sep)[0])

    # Create a new nested dict for each embedded document
    # And add these dicts to the correct top level key
    ed_dict={}
    for ed in eds:
        ed_dict = {}
        for k, v in hyphen_dict.items():
            if ed == k.split(sep)[0]:
                ed_dict[k.split(sep)[1]] = v
        new_dict[ed] = ed_dict

    return new_dict
