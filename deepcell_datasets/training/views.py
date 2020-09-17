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

from deepcell_datasets.database.models import Training_Data


training_bp = Blueprint('training_bp', __name__,  # pylint: disable=C0103
                        template_folder='templates')


@training_bp.errorhandler(Exception)
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


@training_bp.route('/')
def view_all_training_data():
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    training_data = Training_Data.objects.paginate(page=page, per_page=per_page)
    return render_template('training/training-table.html',
                           paginated_training_data=training_data)


@training_bp.route('/<training_data_id>')
def view_training_data(training_data_id):
    training_data = Training_Data.objects.get_or_404(id=training_data_id)
    return render_template('training/training-detail.html',
                           training_data=training_data)
