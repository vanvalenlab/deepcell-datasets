from .db import db

from mongoengine.document import Document
from mongoengine.fields import DateTimeField, StringField, EmailField

# class Images(db.Document):
#     name = db.StringField(required=True, unique=True)
#     casts = db.ListField(db.StringField(), required=True)
#     genres = db.ListField(db.StringField(), required=True)

class Images(Document):
    username = StringField(min_length=4, required=True, unique=True)
    password = StringField(min_length=8, required=True)

    meta = {'db_alias': 'flask_webapp_db'}    # your db name where you want to create the table(Dcoument) Images is your Document(Table) name
    def save(self, force_insert=False, validate=True, clean=True,
         write_concern=None, cascade=None, cascade_kwargs=None,
         _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
        pass