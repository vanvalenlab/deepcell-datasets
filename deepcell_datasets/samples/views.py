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
from flask import current_app
from flask import render_template
from flask import url_for, redirect
from mongoengine import ValidationError

from flask_login import current_user
from flask_security import login_required

from deepcell_datasets.database.models import Samples
from deepcell_datasets.database.models import Experiments

from deepcell_datasets.samples.forms import SampleForm, SampleFilterForm
from deepcell_datasets.utils import nest_dict


samples_bp = Blueprint('samples_bp', __name__,  # pylint: disable=C0103
                       template_folder='templates')


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


# Routes for HTML pages.
# TODO: This should likely be split into several routes allowing
#       users the option to re-use information like scope, step, marker, etc.
#       This could be down with checkbox and passing objects from one route
#       to the next.
@samples_bp.route('/data_entry/<exp_id>', methods=['GET', 'POST'])
@login_required
def add_sample(exp_id):
    form = SampleForm()
    # flask-mongoengine wtf validation fails for required fields
    # TODO: likely a bug in flask-mongo but the following logic shouldnt stay
    if form.validate_on_submit():
        # TODO: This is here to remind us of the package bug:
        current_app.logger.info('Form errors are %s ', form.errors)
        # Do something with data
        body_raw = request.form
        current_app.logger.info('Form body is %s ', body_raw)
        body_dict = nest_dict(body_raw.to_dict())

        # Add in Experiment ID information here
        experiment = Experiments.objects.get_or_404(id=exp_id)
        body_dict['experiment'] = experiment

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


@samples_bp.route('/', methods=['GET'])
@login_required
def view_all_samples():
    page = request.args.get('page', default=1, type=int)

    filters = [
        'experiment',
        'kinetics',
        'spatial_dim',
        'species',
        'specimen',
        'modality__imaging_modality',
        'modality__compartment',
        'modality__marker',
        'imaging_params__platform',
        'imaging_params__magnification',
    ]

    provided_values = (request.args.get(f, default='') for f in filters)
    kwargs = {f: v for f, v in zip(filters, provided_values) if v}

    samples = Samples.objects(**kwargs)

    form = SampleFilterForm()

    per_page = current_app.config['ITEMS_PER_PAGE']
    paginated_samples = samples.paginate(page=page, per_page=per_page)
    return render_template('samples/samples-table.html',
                           paginated_samples=paginated_samples,
                           form=form,
                           **kwargs)


@samples_bp.route('/success')
def success():
    return 'Sample Successfully Submitted'
