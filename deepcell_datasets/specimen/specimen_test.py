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
"""Tests for the Specimen Blueprint."""


def test_get_all_specimen(client):
    # database should be empty
    response = client.get('/specimen/')
    assert response.status_code == 200
    assert response.json == []
    # TODO: add specimen to database and get it again


def test_get_specimen(client):
    specimen_id = 5
    response = client.get('/specimen/%s' % specimen_id)
    assert response.status_code == 200
    assert response.json


def test_create_specimen(client):
    spec_type = ['cell, HEK293']
    ontology_loc = ['dynamic', '2d']
    num_frames = 8
    body = {
        'spec_type': spec_type,
        'ontology_loc': ontology_loc,
        'num_frames': num_frames
    }
    response = client.post('/specimen/', json=body)
    assert response.status_code == 200
    assert response.json


def test_update_specimen(client):
    # no specimens in the collection
    response = client.put('/specimen/')
    assert response.status_code == 200
    assert response.json


def test_delete_specimen(client):
    # no specimens in the collection
    specimen_id = 5
    response = client.delete('/specimen/%s' % specimen_id)
    assert response.status_code == 200
    assert response.json
