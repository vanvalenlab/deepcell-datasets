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
from flask import Response


from database.models import SpecimenType


bp = Blueprint('Deepcell_Datasets', __name__)  # pylint: disable=C0103


@bp.route('/health')
def health():
    """Returns success if the application is ready."""
    return jsonify({'message': 'success'})


@bp.route('/', methods=['GET', 'POST'])
def index():
    """Request HTML landing page to be rendered."""
    return render_template('index.html')


@bp.route('/all_specimen')
def get_all_specimen():
    all_specimen = SpecimenType.objects().to_json()
    # return jsonify({'all_specimen': all_specimen}), 200
    return Response(all_specimen, mimetype="application/json", status=200)


@bp.route('/all_specimen', methods=['POST'])
def create_specimen(name):
    body = request.get_json()
    specimen = SpecimenType(**body).save()
    name = specimen.name
    return jsonify({'name': str(name)}), 200


@bp.route('/all_specimen/<name>', methods=['PUT'])
def update_specimen(name):
    body = request.get_json()
    SpecimenType.objects.get(name=name).update(**body)
    return '', 200


@bp.route('/all_specimen/<name>', methods=['DELETE'])
def delete_specimen(name):
    SpecimenType.objects.get(name=name).delete()
    return '', 200


@bp.route('/all_specimen/<name>')
def get_specimen(name):
    all_specimen = SpecimenType.objects.get(name=name).to_json()
    return Response(all_specimen, mimetype="application/json", status=200)
