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

from flask_security import UserMixin, RoleMixin, MongoEngineUserDatastore

from deepcell_datasets.database.db import db


class Roles(db.Document, RoleMixin):
    """Role assigned to a User, defines access.

    From flask-security-too mognoengine example: https://tinyurl.com/ybc2mslx
    """
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Users(db.Document, UserMixin):
    """A User account.

    From flask-security-too mognoengine example: https://tinyurl.com/ybc2mslx
    """
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Roles), default=[])

    first_name = db.StringField()
    last_name = db.StringField()
    facility = db.StringField()  # Could be Lab here
    # Could include experiments (But only makes sense if it is a different collection)


# TODO: this is NOT a model, but I'm not sure where to put it.
user_datastore = MongoEngineUserDatastore(db, Users, Roles)
# End flask-security setup.


# Begin Data Models
class Methods(db.EmbeddedDocument):
    subtype = db.StringField()
    culture = db.StringField()
    labeling = db.StringField()
    imaging = db.StringField()


class Experiments(db.Document):
    created_by = db.ReferenceField(Users)
    doi = db.StringField()
    date_collected = db.DateTimeField()  # Date on microscope (date added auto-saved by mongo)
    methods = db.EmbeddedDocumentField(Methods)  # Each experiment should have the same methods
    # Specimen + modality + compartment + marker
    # subjects = db.EmbeddedDocumentListField(SpecimenInformation)


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
    z = db.IntField()
    t = db.IntField()


class ModalityInformation(db.EmbeddedDocument):
    # These can't be selected from sets because there could always be a new one
    imaging_modality = db.StringField(required=True)
    compartment = db.StringField()
    marker = db.StringField()


class Samples(db.Document):
    """A single tiff stack or image file.

    This must be a separate collection to facilitate searching across Samples.
    """
    session = db.IntField(required=True)
    position = db.IntField(required=True)
    imaging_params = db.EmbeddedDocumentField(ImagingParameters)
    dimensions = db.EmbeddedDocumentField(Dimensions)
    time_step = db.StringField()
    z_step = db.StringField()

    specimen = db.StringField()
    modality = db.EmbeddedDocumentField(ModalityInformation)

    # Create a custom list field to hold this information
    # kinetics = {'static', 'dynamic'}
    # spatial_dim = {'2d', '3d'}
    # onto_loc = db.StringField(choices=codes.keys(), required = True)
    # But until then use:
    onto_loc = db.ListField(db.StringField())
    # each sample belongs to an Experiment
    experiment = db.ReferenceField(Experiments, reverse_delete_rule=db.NULLIFY)

# Custom Fields
# class OntoLoc(db.ListField):
#     def __init__(self, correct_length=None, **kwargs):
#         self.correct_length = correct_length
#         super(OntoLoc, self).__init__(**kwargs)

#     def validate(self, value):
#         super(OntoLoc, self).validate(value)

#         if self.correct_length is not None and len(value) != self.correct_length:
#             self.error('OntoLoc Information Incorrect')


# # Embedded documents for detailed info that needs context("contains" relationship)
# class RawDataOrigin(db.EmbeddedDocument):
#     facility = db.StringField()
#     collected_by = db.StringField()
#     date_collected = db.DateTimeField()
#     doi = db.StringField()


# class Specimen_Information(db.EmbeddedDocument):
#     tissues_types = db.ListField(db.StringField(), required=True)
#     cells_types = db.ListField(db.StringField(), required=True)
#     dynamic = db.BooleanField()
#     three_dim = db.BooleanField()


# This collection will hold information about each specimen type in our ontology
# class Specimen(db.Document):
#     # Some unique ID for a given specimen within the ontology
#     # Only the combination of spec_id and onto_loc is required to be unique
#     spec_id = db.ListField(db.StringField(), required=True)  # e.g. cell, HEK293
#     ontology_loc = db.ListField(db.StringField(), required=True)  # e.g. dynamic,2d..

#     #experiments = db.ListField(Experiments)  # experiment ID or DOI
#     experiments = db.ListField(db.StringField())  # experiment ID or DOI
#     # DictField for data with unknown structure (how many channels)
#     channel_marker = db.DictField()  # e.g. 0: H2B-mClover, ...

#     meta = {'allow_inheritance': True}


# TODO: Use inheritance to clean the Samples up a bit
#     z_step = db.StringField(required=True)

# class ThreeDimSample(Sample):
#     z_step = db.StringField(required=True)


# TODO: Training data
    # cloud_storage_loc = db.URLField()  # aws address


# TODO: Crowdsourcing
    # How much of data has been sent to f8 and from which dirs
    # a note section on dimensions and amount of raw image used
    # (we sometimes crop out areas because theyre at the edge of dish, etc)
