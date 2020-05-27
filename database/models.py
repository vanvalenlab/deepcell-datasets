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
"""DeepCell MDM Database Models"""

# from mongoengine.document import Document
# from mongoengine.fields import ListField, StringField

from .db import db


class Specimen_Type(db.Document):
    # username = StringField(min_length=4, required=True, unique=True)
    # password = StringField(min_length=8, required=True)

    name = db.StringField(required=True, unique=True)  # Specimen Name

    # For each specimen it will be one "row" per .tif stack
    spec_type = db.ListField(db.StringField(), required=True)  # e.g. cell, HEK293
    channel_marker = db.ListField(db.StringField(), required=True) # e.g. 0: H2B-mClover, ...
    exp_id = db.StringField(required=True)  # experiment ID or DOI


    # def save(self, force_insert=False, validate=True, clean=True,
    # 		 write_concern=None, cascade=None, cascade_kwargs=None,
    # 		 _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
    # 	pass
