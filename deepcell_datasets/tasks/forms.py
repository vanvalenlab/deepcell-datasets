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
"""Forms for Samples."""

from wtforms import fields, validators
from flask_wtf import FlaskForm


class DimensionsForm(FlaskForm):
    x = fields.IntegerField('x', validators=[validators.required()])
    y = fields.IntegerField('y', validators=[validators.required()])
    z = fields.IntegerField('z')
    t = fields.IntegerField('t')


class TaskForm(FlaskForm):
    """Form for creating a new Samples document."""

    coordinate_x = fields.IntegerField()
    coordinate_y = fields.IntegerField()
    coordinate_z = fields.IntegerField()
    coordinate_t = fields.IntegerField()

    platform = fields.RadioField(choices=('appen', 'anolytics', 'mturk'),
                                 validators=[validators.required()])

    project_ids = fields.StringField()

    dimensions = fields.FormField(DimensionsForm)

    date_submitted = fields.StringField()
    date_completed = fields.StringField()

    queued = fields.BooleanField()
    annotated = fields.BooleanField()
    curated = fields.BooleanField()

    cloud_storage_loc = fields.StringField()  # can use .html5.URLField
    nas_filepath = fields.StringField()


class TaskFilterForm(FlaskForm):
    """Form for querying Sample documents."""

    platform = fields.RadioField(choices=('', 'appen', 'anolytics', 'mturk'))
