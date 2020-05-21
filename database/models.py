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
