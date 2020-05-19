"""Flask blueprint for modular routes."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import distutils
import json
import os
import re

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import current_app

from models import Project


bp = Blueprint('deepcell_datasets', __name__)  # pylint: disable=C0103


@bp.route('/health')
def health():
    '''Returns success if the application is ready.'''
    return jsonify({'message': 'success'})