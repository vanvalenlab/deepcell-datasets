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

from deepcell_datasets.database.db import db


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
    num_frames = db.IntField(required=True)


class Specimen_Information(db.EmbeddedDocument):
    tissues_types = db.ListField(db.StringField(), required=True)
    cells_types = db.ListField(db.StringField(), required=True)
    dynamic = db.BooleanField()
    three_dim = db.BooleanField()

class Experiments(db.Document):
    data_origin = db.EmbeddedDocumentField(RawDataOrigin)  # Embedded documents for "contains" relationships
    doi = db.StringField()  # Could be DOI or made from data_origin (user+date)
    specimen_types = db.EmbeddedDocumentField(Specimen_Information)
    methods = db.EmbeddedDocumentField(Methods)  # Each experiment should have the same methods

# This collection will hold information about each specimen type in our ontology
class Specimen(db.Document):
    # Some unique ID for a given specimen within the ontology
    # Only the combination of spec_id and onto_loc is required to be unique
    spec_id = db.ListField(db.StringField(), required=True)  # e.g. cell, HEK293
    ontology_loc = db.ListField(db.StringField(), required=True)  # e.g. dynamic,2d..

    #experiments = db.ListField(Experiments)  # experiment ID or DOI
    experiments = db.ListField(db.StringField())  # experiment ID or DOI
    # DictField for data with unknown structure (how many channels)
    channel_marker = db.DictField()  # e.g. 0: H2B-mClover, ...

# Each document in this collection equates to one .tif stack
# Needs the Context of Sepcimen+Channel_Marker+Experiment to be useful
class Sample(db.EmbeddedDocument):
    # A unique ID can be formed from session and position
    session = db.IntField(required=True)
    position = db.IntField(required=True)
    imaging_params = db.EmbeddedDocumentField(ImagingParameters)
    dimensions = db.EmbeddedDocumentField(Dimensions)
    time_step = db.StringField()
    z_step = db.StringField()

    meta = {'allow_inheritance': True}

# TODO: Use inheritance to clean the Samples up a bit
# class DynamicSample(Sample):
#     time_step = db.StringField(required=True)

# class ThreeDimSample(Sample):
#     z_step = db.StringField(required=True)



# TODO: Training data
    # cloud_storage_loc = db.URLField()  # aws address


# TODO: Crowdsourcing
    # How much of data has been sent to f8 and from which dirs
    # a note section on dimensions and amount of raw image used
    # (we sometimes crop out areas because theyre at the edge of dish, etc)
