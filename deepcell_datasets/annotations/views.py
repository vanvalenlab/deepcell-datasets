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

from flask_login import current_user
from flask_security import login_required

from mongoengine import ValidationError

from deepcell_datasets.database.models import Annotations
from deepcell_datasets.annotations.forms import AnnotationForm
from deepcell_datasets.utils import nest_dict
# TODO: finish tasks bp
# from deepcell_datasets.tasks.views import tasks_bp


annotations_bp = Blueprint('annotations_bp', __name__,  # pylint: disable=C0103
                           template_folder='templates')


@annotations_bp.errorhandler(Exception)
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


# Routes for HTML pages.
@annotations_bp.route('/data_entry', methods=['GET', 'POST'])
@login_required
def add_annotation():
    form = AnnotationForm()
    if form.validate_on_submit():
        body_raw = request.form
        current_app.logger.info('Form body is %s ', body_raw)
        body_dict = nest_dict(body_raw.to_dict())
        # Add in current user information
        body_dict['submitted_by'] = current_user._get_current_object()

        current_app.logger.info('Nested dict to save is %s ', body_dict)
        annotation = Annotations(**body_dict).save()

        current_app.logger.info('annotation %s saved succesfully', annotation)
        unique_id = annotation.id
        current_app.logger.info('unique_id %s extracted as key', unique_id)

        # TODO: It would be helpful to have the annotation added to the User
        #       collection here

        return redirect(url_for('tasks_bp.add_task', ann_id=unique_id))
    return render_template('annotations/data_entry.html',
                           form=form,
                           current_user=current_user)


@annotations_bp.route('/', methods=['GET'])
@login_required
def view_all_annotations():
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']

    filters = [
        'methods__subtype',
        'methods__culture',
        'methods__labeling',
        'methods__imaging',
    ]

    provided_values = (request.args.get(f, default='') for f in filters)
    kwargs = {f: v for f, v in zip(filters, provided_values) if v}

    annotations = Annotations.objects(**kwargs)

    paginated_annotations = annotations.paginate(page=page, per_page=per_page)
    return render_template('annotations/annotations-table.html',
                           paginated_annotations=paginated_annotations)


@annotations_bp.route('/<annotation_id>', methods=['GET'])
@login_required
def view_annotation(annotation_id):
    annotation = Annotations.objects.get_or_404(id=annotation_id)
    return render_template('annotations/annotation-detail.html',
                           annotation=annotation)


@annotations_bp.route('/success')
def success():
    # TODO: render HTML template, maybe forward to "My Annotations"
    return 'Annotation Successfully Submitted'