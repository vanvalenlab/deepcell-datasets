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

from deepcell_datasets.database.models import Tasks
from deepcell_datasets.database.models import Annotations

from deepcell_datasets.tasks.forms import TaskForm, TaskFilterForm
from deepcell_datasets.utils import nest_dict


tasks_bp = Blueprint('tasks_bp', __name__,  # pylint: disable=C0103
                       template_folder='templates')


@tasks_bp.errorhandler(Exception)
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
@tasks_bp.route('/data_entry/<ann_id>', methods=['GET', 'POST'])
@login_required
def add_task(ann_id):
    form = TaskForm()
    # flask-mongoengine wtf validation fails for required fields
    # TODO: likely a bug in flask-mongo but the following logic shouldnt stay
    if form.validate_on_submit():
        # TODO: This is here to remind us of the package bug:
        current_app.logger.info('Form errors are %s ', form.errors)
        # Do something with data
        body_raw = request.form
        current_app.logger.info('Form body is %s ', body_raw)
        body_dict = nest_dict(body_raw.to_dict())

        # Add in Annotation ID information here
        annotation = Annotations.objects.get_or_404(id=ann_id)
        body_dict['annotation'] = annotation

        current_app.logger.info('Nested dict to save is %s ', body_dict)
        task = Tasks(**body_dict).save()

        current_app.logger.info('task %s saved succesfully', task)
        unique_id = task.id
        current_app.logger.info('unique_id %s extracted as key', unique_id)

        return redirect(url_for('tasks_bp.success'))

    return render_template('tasks/data_entry.html',
                           form=form,
                           current_user=current_user,
                           ann_id=ann_id)


@tasks_bp.route('/', methods=['GET'])
@login_required
def view_all_tasks():
    page = request.args.get('page', default=1, type=int)

    filters = [
        'annotation',
        'platform',
    ]

    provided_values = (request.args.get(f, default='') for f in filters)
    kwargs = {f: v for f, v in zip(filters, provided_values) if v}

    tasks = Tasks.objects(**kwargs)

    form = TaskFilterForm()

    per_page = current_app.config['ITEMS_PER_PAGE']
    paginated_tasks = tasks.paginate(page=page, per_page=per_page)
    return render_template('tasks/tasks-table.html',
                           paginated_tasks=paginated_tasks,
                           form=form,
                           **kwargs)


@tasks_bp.route('/success')
def success():
    return 'Task Successfully Submitted'
