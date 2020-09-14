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
"""Tests for the Training_Data Blueprint."""

import random

import pytest
from mongoengine import DoesNotExist

from deepcell_datasets.database import models


def new_training_data():
    """Create new training data with some static values"""
    cloud_storage_loc = 'https://deepcell.org'
    training_data = models.Training_Data(
        cloud_storage_loc=cloud_storage_loc,
        kinetics=random.choice(['static', 'dynamic']),
        spatial_dim=random.choice(['2d', '3d']),
    )
    training_data.save()
    return training_data


def test_get_all_training_data(client):
    # database should be empty
    response = client.get('/api/training/')
    assert response.status_code == 200
    assert response.json == []

    # create new training_data get all again.
    training_data = new_training_data()
    response = client.get('/api/training/')
    assert len(response.json) == 1
    assert response.json[0]['cloud_storage_loc'] == training_data.cloud_storage_loc
    training_data.delete()


def test_get_training_data(client):
    training_data = new_training_data()
    response = client.get('/api/training/%s' % training_data.id)
    assert response.status_code == 200
    assert response.json['cloud_storage_loc'] == training_data.cloud_storage_loc

    # test bad training_data ID
    response = client.get('/api/training/%s' % 5)
    assert response.status_code == 404
    training_data.delete()


# def test_create_training_data(client):
#     doi = str(random.randint(1, 1000))
#     body = {'cloud_storage_loc': 'https://google.com/{}'.format(doi)}
#     response = client.post('/api/training/', json=body)
#     assert response.status_code == 200
#     unique_id = response.json['unique_id']
#     assert unique_id is not None
#     # test that the ID exists in the database
#     training_data = models.Training_Data.objects.get(id=unique_id)
#     assert training_data.cloud_storage_loc == doi
#     assert str(training_data.id) == str(unique_id)
#     # TODO: test bad body payload, no required fields currently.
#     # bad_body = {'cloud_storage_loc': None}
#     # response = client.post('/api/training_datas/', json=bad_body)
#     # assert response.status_code == 400
#     training_data.delete()


# def test_update_training_data(client):
#     training_data = new_training_data()
#     new_url = 'https://test.com/a different URL'
#     payload = {'cloud_storage_loc': new_url}
#     response = client.put('/api/training/%s' % training_data.id, json=payload)
#     assert response.status_code == 204
#     updated = models.Training_Data.objects.get(id=training_data.id)
#     assert updated.cloud_storage_loc == new_url

#     # test bad training_data ID
#     response = client.put('/api/training/%s' % 1, json=payload)
#     assert response.status_code == 404
#     training_data.delete()


# def test_delete_training_data(client):
#     training_data = new_training_data()
#     response = client.delete('/api/training/%s' % training_data.id)
#     assert response.status_code == 204
#     with pytest.raises(DoesNotExist):
#         models.Training_Data.objects.get(id=training_data.id)

#     # test bad training_data ID
#     response = client.delete('/api/training/%s' % training_data.id)
#     assert response.status_code == 404
#     training_data.delete()
