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
"""Flask blueprint for Task data API."""

from werkzeug.exceptions import HTTPException
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from flask import current_app

from mongoengine import ValidationError

from deepcell_datasets.database.models import Tasks


tasks_api_bp = Blueprint('tasks_api_bp', __name__,  # pylint: disable=C0103
                           template_folder='templates')


@tasks_api_bp.errorhandler(Exception)
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


@tasks_api_bp.route('/')
def get_tasks():  # def get_tasks(page=1):
    # paginated_tasks = Tasks.objects.paginate(page=page, per_page=10)
    tasks = Tasks.objects().to_json()
    return Response(tasks, mimetype='application/json')


@tasks_api_bp.route('/', methods=['POST'])
def create_task():
    """Create a new task"""
    body = request.get_json()
    current_app.logger.info('Body is %s ', body)
    task = Tasks(**body).save()
    current_app.logger.info('task %s saved succesfully', task)
    unique_id = task.id
    current_app.logger.info('unique_id %s extracted as key', unique_id)
    return jsonify({'unique_id': str(unique_id)})


@tasks_api_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    body = request.get_json()
    Tasks.objects.get_or_404(id=task_id).update(**body)
    return jsonify({}), 204  # successful update but no content


@tasks_api_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    Tasks.objects.get_or_404(id=task_id).delete()
    return jsonify({}), 204  # successful delete but no content


@tasks_api_bp.route('/<task_id>')
def get_task(task_id):
    task = Tasks.objects.get_or_404(id=task_id).to_json()
    return Response(task, mimetype='application/json')
