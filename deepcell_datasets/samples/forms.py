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


class ImagingParametersForm(FlaskForm):
    microscope = fields.StringField('Microscope')
    camera = fields.StringField('Camera')
    magnification = fields.FloatField(
        'Magnification (e.g. 40x)', validators=[validators.NumberRange(0)])
    na = fields.FloatField('NA', validators=[validators.NumberRange(0, 5)])
    binning = fields.StringField('Binning', validators=[validators.Length(0, 1000)])
    pixel_size = fields.StringField('Pixel Size', validators=[validators.Length(0, 255)])
    exposure_time = fields.StringField('Exposure Time', validators=[validators.Length(0, 255)])


class DimensionsForm(FlaskForm):
    x = fields.IntegerField('x', validators=[validators.required()])
    y = fields.IntegerField('y', validators=[validators.required()])
    z = fields.IntegerField('z')
    t = fields.IntegerField('t')


class ModalityInformationForm(FlaskForm):
    imaging_modality = fields.StringField(
        'Imaging Modality', validators=[validators.required()])
    compartment = fields.StringField(
        'Compartment of Interest', validators=[validators.Length(0, 1000)])
    marker = fields.StringField('Marker', validators=[validators.Length(0, 1000)])


class SampleForm(FlaskForm):
    """Form for creating a new Samples document."""

    session = fields.IntegerField('Session',
                                  validators=[validators.required()])
    position = fields.IntegerField('Sample Position/FOV',
                                   validators=[validators.required()])

    time_step = fields.StringField('Time Step', validators=[validators.Length(0, 255)])
    z_step = fields.StringField('Z Step', validators=[validators.Length(0, 255)])

    specimen = fields.StringField('Specimen Name',
                                  validators=[validators.Length(0, 1000)])

    # imaging parameters (embedded document fields)
    imaging_params = fields.FormField(ImagingParametersForm)

    # dimensions (embedded document fields)
    dimensions = fields.FormField(DimensionsForm)

    # modality (embedded document fields)
    modality = fields.FormField(ModalityInformationForm)

    # location in the ontology
    kinetics = fields.RadioField(choices=('static', 'dynamic'),
                                 validators=[validators.required()])
    spatial_dim = fields.RadioField(choices=('2d', '3d'),
                                    validators=[validators.required()])

class SampleFilterForm(FlaskForm):
    """Form for querying Sample documents."""

    # location in the ontology
    kinetics = fields.RadioField(choices=('', 'static', 'dynamic'))

    spatial_dim = fields.RadioField(choices=('', '2d', '3d'))
