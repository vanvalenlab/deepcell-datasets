from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask_mongoengine import MongoEngine


db = MongoEngine()


def initialize_db(app):
    db.init_app(app)
