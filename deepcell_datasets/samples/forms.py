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
"""Forms for Saples."""

from flask_mongoengine.wtf import model_form

from deepcell_datasets.database.models import Samples
from deepcell_datasets.database.models import ImagingParameters
from deepcell_datasets.database.models import Dimensions
from deepcell_datasets.database.models import ModalityInformation

# Should this exclude created_by as we will add this through current_user
# BaseForm = model_form(Samples,
#                       field_args={'kinetics': {'radio': True},
#                                   'spatial_dim': {'radio': True}})
BaseForm = model_form(Samples)
BaseFormW_img = model_form(ImagingParameters, BaseForm)
BaseFormW_img_dim = model_form(Dimensions, BaseFormW_img)

SampleForm = model_form(ModalityInformation, BaseFormW_img_dim)
