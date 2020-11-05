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
"""Tests for the Annotation Blueprint."""

import random

import pytest
from mongoengine import DoesNotExist

from deepcell_datasets.database import models


def new_annotation():
    """Create new annotation with some static values"""
    doi = 'a doi value'
    annotation = models.Annotations(doi=doi)
    annotation.save()
    return annotation


def test_get_all_annotation(client):
    # database should be empty
    response = client.get('/api/annotations/')
    assert response.status_code == 200
    assert response.json == []

    # create new annotation get all again.
    annotation = new_annotation()
    response = client.get('/api/annotations/')
    assert len(response.json) == 1
    assert response.json[0]['doi'] == annotation.doi
    annotation.delete()


def test_get_annotation(client):
    annotation = new_annotation()
    response = client.get('/api/annotations/%s' % annotation.id)
    assert response.status_code == 200
    assert response.json['doi'] == annotation.doi

    # test bad annotation ID
    response = client.get('/api/annotations/%s' % 5)
    assert response.status_code == 404
    annotation.delete()


def test_create_annotation(client):
    doi = str(random.randint(1, 1000))
    body = {'doi': doi}
    response = client.post('/api/annotations/', json=body)
    assert response.status_code == 200
    unique_id = response.json['unique_id']
    assert unique_id is not None
    # test that the ID exists in the database
    annotation = models.Annotations.objects.get(id=unique_id)
    assert annotation.doi == doi
    assert str(annotation.id) == str(unique_id)
    # TODO: test bad body payload, no required fields currently.
    # bad_body = {'doi': None}
    # response = client.post('/api/annotations/', json=bad_body)
    # assert response.status_code == 400
    annotation.delete()


def test_update_annotation(client):
    annotation = new_annotation()
    new_doi = 'a different DOI value'
    payload = {'doi': new_doi}
    response = client.put('/api/annotations/%s' % annotation.id, json=payload)
    assert response.status_code == 204
    updated = models.Annotations.objects.get(id=annotation.id)
    assert updated.doi == new_doi

    # test bad annotation ID
    response = client.put('/api/annotations/%s' % 1, json=payload)
    assert response.status_code == 404
    annotation.delete()


def test_delete_annotation(client):
    annotation = new_annotation()
    response = client.delete('/api/annotations/%s' % annotation.id)
    assert response.status_code == 204
    with pytest.raises(DoesNotExist):
        models.Annotations.objects.get(id=annotation.id)

    # test bad annotation ID
    response = client.delete('/api/annotations/%s' % annotation.id)
    assert response.status_code == 404
    annotation.delete()
