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
    roles = db.ListField(db.ReferenceField(Roles), default=[])

    # Required for confirmable Users
    confirmed_at = db.DateTimeField()

    # Required fields for user login tracking: SECURITY_TRACKABLE
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField(max_length=64)
    current_login_ip = db.StringField(max_length=64)
    login_count = db.IntField()

    first_name = db.StringField()
    last_name = db.StringField()
    lab_group = db.StringField()  # e.g. DVV
    facility = db.StringField()  # Could be building/institution/etc
    experiments = db.ListField(db.StringField())  # experiment ID


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
    doi = db.StringField(max_length=1000)  # Name/ID field in addtion to this?
    date_collected = db.StringField()  # Date on microscope (date added auto-saved by mongo)
    methods = db.EmbeddedDocumentField(Methods)  # Each experiment should have the same methods
    copyright = db.StringField()
    # Specimen + modality + compartment + marker
    # subjects = db.EmbeddedDocumentListField(SpecimenInformation)


class ImagingParameters(db.EmbeddedDocument):
    platform = db.StringField()
    microscope = db.StringField()
    camera = db.StringField()
    magnification = db.FloatField(required=True, min_value=0)  # objective?
    na = db.FloatField(min_value=0, max_value=5)
    binning = db.StringField(max_length=1000)
    pixel_size = db.FloatField(required=True)  # assume um per pixel
    exposure_time = db.StringField(max_length=255)


class Dimensions(db.EmbeddedDocument):
    x = db.IntField(required=True)
    y = db.IntField(required=True)
    z = db.IntField()
    t = db.IntField()


class ModalityInformation(db.EmbeddedDocument):
    # These can't be selected from sets because there could always be a new one
    imaging_modality = db.StringField(required=True, max_length=1000)
    compartment = db.StringField(required=True, max_length=1000)
    marker = db.StringField(required=True, max_length=1000)  # TODO: Should this be a list? multiple for whole_cell or cyto+nuc in one image


class Samples(db.Document):
    """A single tiff stack or image file.

    This must be a separate collection to facilitate searching across Samples.
    """
    session = db.IntField(required=True)
    position = db.IntField(required=True)
    imaging_params = db.EmbeddedDocumentField(ImagingParameters)
    dimensions = db.EmbeddedDocumentField(Dimensions)
    time_step = db.StringField(max_length=255)
    z_step = db.StringField(max_length=255)

    species = db.StringField(max_length=1000)
    specimen = db.StringField(max_length=1000)
    modality = db.EmbeddedDocumentField(ModalityInformation)

    # location in the ontology
    kinetics = db.StringField(choices=('static', 'dynamic'), required=True)
    spatial_dim = db.StringField(choices=('2d', '3d'), required=True)

    # each sample belongs to an Experiment
    experiment = db.ReferenceField(Experiments, required=True, reverse_delete_rule=db.NULLIFY)


# TODO: Finish Crowdsourcing


class Subsection(db.EmbeddedDocument):
    coordinate_x = db.IntField()
    coordinate_y = db.IntField()
    coordinate_z = db.IntField()
    coordinate_t = db.IntField()

    dimensions = db.EmbeddedDocumentField(Dimensions)

    queued = db.BooleanField()
    annotated = db.BooleanField()
    curated = db.BooleanField()  # Could also be QCd?

# TODO: crowdsourcing and subsection should be inversed. proj id and sample id belong
# to subsection not the other way around
class Crowdsourcing(db.Document):
    """This should describe which samples have been sent to which crowdsourcing companies.
    It should also note what dimensions were used and what area of the original raw image
    it came from (we sometimes crop out areas because theyre at the edge of dish, etc).

    Should we state/force standard dimensions here?
    """

    # Should be connected to individual samples

    platform = db.StringField(choices=('appen', 'anolytics', 'mturk'), required=True)
    submitted_by = db.ReferenceField(Users)

    subsections = db.EmbeddedDocumentField(Subsection)

    split_seed = db.IntField()  # Fed into caliban-toolbox to create train/val/test split

# TODO: Finish Training data


class annotation_stats(db.EmbeddedDocument):
    # TODO: include total number of annotations/trajectories/children
    num_batches = db.IntField()  # for 2d this is num imgs, for 3d num movies, etc
    dimensions = db.EmbeddedDocumentField(Dimensions)
    num_ann = db.IntField()
    num_div = db.IntField()


class Training_Data(db.Document):
    """A collection of pointers to each npz containing paired X(raw) and y(annotations) data.

    """
    # location in the ontology (the annotation could be different than the raw data
    # e.g. movies vs indpendent imgs)
    kinetics = db.StringField(choices=('static', 'dynamic'), required=True)
    spatial_dim = db.StringField(choices=('2d', '3d'), required=True)
    annotation_type = db.StringField()  # whole cell, cyto, nuc, AM, tracking, dots?

    # ID information
    doi = db.StringField(max_length=1000)  # DOI may be different than raw (compliation of multiple)
    title = db.StringField()  # Human-readable for display purpose (eg. smith et al. nuclear study)
    copyright = db.StringField()

    # Samples contained or link to crowdsourcing (individual annotated pieces of samples)?
    samples_contained = db.ListField(db.ReferenceField(Samples), reverse_delete_rule=db.NULLIFY)
    # TODO: Should have coordinates that follow samples and subsamples
    # TODO: Is samples_contained sufficient? Should keys like tissue/platform list be stored here?
    # TODO: does channel_list violate our data ontology? shouldnt it be 1-to-1?
    raw_channel_list = db.ListField(db.StringField())  # TODO: Should this be DNA/Membrane or dsDNA or DAPI or nuc?
    # TODO: Which samples/platforms exist with which batch? Do we need a one-to-one like that?
    padding = db.BooleanField()
    # TODO: Include size of padding (x and y)

    ann_version = db.StringField()  # TODO: Link this to DVC
    last_modified = db.StringField()
    ann_stats = db.EmbeddedDocumentField(annotation_stats)

    split_train = db.FloatField()  # Percentage of total data in train
    split_val = db.FloatField()
    split_test = db.FloatField()

    raw_dtype = db.StringField()  # TODO: Enumerate as choices
    ann_dtype = db.StringField()

    nas_filepath = db.StringField()  # path to the npz on madrox
    cloud_storage_loc = db.URLField()  # aws address


# TODO: Use inheritance to clean the Samples up a bit (dynamic/static, 2D/3D)
#     meta = {'allow_inheritance': True}

# Custom Fields
# class OntoLoc(db.ListField):
#     def __init__(self, correct_length=None, **kwargs):
#         self.correct_length = correct_length
#         super(OntoLoc, self).__init__(**kwargs)

#     def validate(self, value):
#         super(OntoLoc, self).validate(value)

#         if self.correct_length is not None and len(value) != self.correct_length:
#             self.error('OntoLoc Information Incorrect')
