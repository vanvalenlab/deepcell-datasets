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

import pytest

from mongoengine import DoesNotExist

from deepcell_datasets.database import models


def new_specimen():
    # TODO: clean up these created items after the test.
    """Create new specimen with some static values"""
    spec_id = ['cell', 'HEK293']
    ontology_loc = ['dynamic', '2d']
    specimen = models.Specimen(
        spec_id=spec_id,
        ontology_loc=ontology_loc
    )
    specimen.save()
    return specimen


def test_get_all_specimen(client):
    # database should be empty
    response = client.get('/specimen/')
    assert response.status_code == 200
    assert response.json == []

    # create new specimen get all again.
    specimen = new_specimen()
    response = client.get('/specimen/')
    assert len(response.json) == 1
    assert response.json[0]['spec_id'] == specimen.spec_id
    assert response.json[0]['ontology_loc'] == specimen.ontology_loc


def test_get_specimen(client):
    specimen = new_specimen()
    response = client.get('/specimen/%s' % specimen.id)
    assert response.status_code == 200
    assert response.json['spec_id'] == specimen.spec_id
    assert response.json['ontology_loc'] == specimen.ontology_loc

    # test bad specimen ID
    response = client.get('/specimen/%s' % 5)
    assert response.status_code == 404


def test_create_specimen(client):
    spec_id = ['cell, HEK293']
    ontology_loc = ['dynamic', '2d']
    body = {
        'spec_id': spec_id,
        'ontology_loc': ontology_loc
    }
    response = client.post('/specimen/', json=body)
    assert response.status_code == 200
    unique_id = response.json['unique_id']
    assert unique_id is not None
    # test that the ID exists in the database
    specimen = models.Specimen.objects.get(id=unique_id)
    assert specimen.spec_id == spec_id
    assert specimen.ontology_loc == ontology_loc
    assert str(specimen.id) == str(unique_id)
    # test bad body payload
    bad_body = {'spec_id': spec_id}
    response = client.post('/specimen/', json=bad_body)
    assert response.status_code == 500


def test_update_specimen(client):
    specimen = new_specimen()
    new_ontology = ['new', 'values']
    payload = {
        'ontology_loc': new_ontology
    }
    response = client.put('/specimen/%s' % specimen.id, json=payload)
    assert response.status_code == 204
    updated = models.Specimen.objects.get(id=specimen.id)
    assert updated.ontology_loc == new_ontology

    # test bad specimen ID
    response = client.put('/specimen/%s' % 1, json=payload)
    assert response.status_code == 404


def test_delete_specimen(client):
    specimen = new_specimen()
    response = client.delete('/specimen/%s' % specimen.id)
    assert response.status_code == 204
    with pytest.raises(DoesNotExist):
        models.Specimen.objects.get(id=specimen.id)

    # test bad specimen ID
    response = client.delete('/specimen/%s' % specimen.id)
    assert response.status_code == 404
