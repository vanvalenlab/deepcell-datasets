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
from mongoengine import ValidationError

from flask_login import current_user
from flask_security import login_required
from flask_mongoengine.wtf import model_form

from deepcell_datasets.database.models import Samples
from deepcell_datasets.database.models import ImagingParameters
from deepcell_datasets.database.models import Dimensions
from deepcell_datasets.database.models import ModalityInformation


samples_bp = Blueprint('samples_bp', __name__,  # pylint: disable=C0103
                       template_folder='templates')


# TODO: It would be better for this to live in a 'forms' module
# Should this exclude created_by as we will add this through current_user
BaseForm = model_form(Samples,
                      field_args={'kinetics': {'radio': True},
                                  'spatial_dim': {'radio': True}})
BaseFormW_img = model_form(ImagingParameters, BaseForm)
BaseFormW_img_dim = model_form(Dimensions, BaseFormW_img)

SampleForm = model_form(ModalityInformation, BaseFormW_img_dim)


@samples_bp.errorhandler(Exception)
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
    return jsonify({'error': str(err)}), 500


@samples_bp.route('/')
def get_samples():  # def get_samples(page=1):
    # paginated_samples = Samples.objects.paginate(page=page, per_page=10)
    samples = Samples.objects().to_json()
    return Response(samples, mimetype='application/json')


@samples_bp.route('/', methods=['POST'])
def create_sample():
    """Create a new experiments"""
    body = request.get_json()
    current_app.logger.info('Body is %s ', body)
    sample = Samples(**body).save()
    current_app.logger.info('sample %s saved succesfully', sample)
    unique_id = sample.id
    current_app.logger.info('unique_id %s extracted as key', unique_id)
    return jsonify({'unique_id': str(unique_id)})


@samples_bp.route('/<sample_id>', methods=['PUT'])
def update_sample(sample_id):
    body = request.get_json()
    Samples.objects.get_or_404(id=sample_id).update(**body)
    return jsonify({}), 204  # successful update but no content


@samples_bp.route('/<sample_id>', methods=['DELETE'])
def delete_sample(sample_id):
    Samples.objects.get_or_404(id=sample_id).delete()
    return jsonify({}), 204  # successful update but no content


@samples_bp.route('/<sample_id>')
def get_sample(sample_id):
    sample = Samples.objects.get_or_404(id=sample_id).to_json()
    return Response(sample, mimetype='application/json')


# Routes for HTML pages.
@samples_bp.route('/data_entry/<exp_id>', methods=['GET', 'POST'])
@login_required
def add_sample(exp_id):
    form = SampleForm()
    if form.validate_on_submit():
        # Do something with data
        body_raw = request.form
        current_app.logger.info('Form body is %s ', body_raw)

        body_dict = nest_dict(body_raw.to_dict())
        current_app.logger.info('Nested dict to save is %s ', body_dict)
        sample = Samples(**body_dict).save()

        current_app.logger.info('sample %s saved succesfully', sample)
        unique_id = sample.id
        current_app.logger.info('unique_id %s extracted as key', unique_id)


        return redirect(url_for('samples_bp.success'))
    return render_template('samples/data_entry.html',
                           form=form,
                           current_user=current_user,
                           exp_id=exp_id)


@samples_bp.route('/success')
def success():
    return 'Sample Successfully Submitted'


# TODO: This shared utility should not live here permanently
# Utility functions
def nest_dict(flat_dict, sep='-'):
    """Return nested dict by splitting the keys on a delimiter.

    """

    # Start a new dict to hold top level keys and take values for these top level keys
    new_dict = {}
    hyphen_dict = {}
    eds = set()
    for k, v in flat_dict.items():
        if '-' not in k:
            new_dict[k] = v
        else:
            hyphen_dict[k] = v
            eds.add(k.split(sep)[0])

    # Create a new nested dict for each embedded document
    # And add these dicts to the correct top level key
    ed_dict = {}
    for ed in eds:
        ed_dict = {}
        for k, v in hyphen_dict.items():
            if ed == k.split(sep)[0]:
                ed_dict[k.split(sep)[1]] = v
        new_dict[ed] = ed_dict

    return new_dict