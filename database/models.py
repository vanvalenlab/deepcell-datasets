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

# This collection will hold information about each specimen type in our ontology
class Experiments(db.document):
    _id = db.StringField(required=True, unique=True) # Experiment ID or DOI

# Embedded documents for detailed info that needs context("contains" relationship)
class RawDataOrigin(db.EmbeddedDocument):
    facility = db.StringField()
    collected_by = db.StringField()
    date_collected = db.DateTimeField()
    doi = db.StringField()

class Methods(db.EmbeddedDocument):
    subtype = db.StringField()
    culture = db.StringField()
    labeling = db.StringField()
    imaging = db.StringField()

class ImagingParameters(db.EmbeddedDocument):
    microscope = db.StringField()
    camera = db.StringField()
    magnification = db.FloatField(min_value=0)
    na = db.FloatField(min_value=0, max_value=5)
    binning = db.StringField()
    pixel_size = db.StringField()
    exposure_time = db.StringField()

class Dimensions(db.EmbeddedDocument):
    x = db.IntField(required=True)
    y = db.IntField(required=True)

# For each specimen it will be one "row" per .tif stack
# Raw data
class Specimen(db.Document):

    exp_id = db.ReferenceField(Experiments, reverse_delete_rule=CASCADE)  # experiment ID or DOI
    spec_type = db.ListField(db.StringField(), required=True)  # e.g. cell, HEK293
    ontology_loc = db.ListField(db.StringField, required=True) #e.g. dynamic,2d..
    num_frames = db.IntField(required=True)
    # Embedded documents for "contains" relationships
    data_origin = db.EmbeddedDocumentField(RawDataOrigin)
    methods = db.EmbeddedDocumentField(Methods)
    imaging_params = db.EmbeddedDocumentField(ImagingParameters)
    dimensions = db.EmbeddedDocumentField(Dimensions)
    # DictField for data with unknown structure (how many channels)
    channel_marker = db.DictField() # e.g. 0: H2B-mClover, ...

    meta = {'allow_inheritance': True}

class DynamicSpecimen(Specimen):
    time_step = db.StringField(required=True)

class ThreeDimSpecimen(Specimen):
    z_step = db.StringField(required=True)


# TODO: Training data
    # cloud_storage_loc = db.URLField()  # aws address


# TODO: Crowdsourcing