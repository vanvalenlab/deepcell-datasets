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

import random

import pytest
from mongoengine import DoesNotExist
from mongomock import ObjectId

from deepcell_datasets.database import models


def new_sample(experiment_id):
    """Create new sample with some static values"""
    # Defined required fields
    session = 1
    position = 2
    spatial_dim = random.choice(['2d', '3d'])
    kinetics = random.choice(['static', 'dynamic'])

    # Create the sample
    sample = models.Samples(
        session=session,
        position=position,
        spatial_dim=spatial_dim,
        kinetics=kinetics,
        experiment=experiment_id,
    )
    sample.save()
    return sample


def test_get_all_sample(client, experiment):
    # database should be empty
    response = client.get('/api/samples/')
    assert response.status_code == 200
    assert response.json == []

    # create new sample get all again.
    sample = new_sample(experiment.id)
    response = client.get('/api/samples/')
    assert len(response.json) == 1
    assert response.json[0]['session'] == sample.session
    assert response.json[0]['position'] == sample.position
    sample.delete()


def test_get_sample(client, experiment):
    sample = new_sample(experiment.id)
    response = client.get('/api/samples/%s' % sample.id)
    assert response.status_code == 200
    assert response.json['session'] == sample.session
    assert response.json['position'] == sample.position

    # test bad sample ID
    response = client.get('/api/samples/%s' % ObjectId())
    assert response.status_code == 404
    sample.delete()


def test_create_sample(client, experiment):
    session = random.randint(1, 1000)
    position = random.randint(1, 1000)
    spatial_dim = random.choice(['2d', '3d'])
    kinetics = random.choice(['static', 'dynamic'])
    body = {
        'session': session,
        'position': position,
        'spatial_dim': spatial_dim,
        'kinetics': kinetics,
        'experiment': str(experiment.id),
    }
    response = client.post('/api/samples/', json=body)
    assert response.status_code == 200
    unique_id = response.json['unique_id']
    assert unique_id is not None
    # test that the ID exists in the database
    sample = models.Samples.objects.get(id=unique_id)
    assert sample.session == session
    assert sample.position == position
    assert str(sample.id) == str(unique_id)
    # test bad body payload
    bad_body = {'session': 0}
    response = client.post('/api/samples/', json=bad_body)
    assert response.status_code == 400


def test_update_sample(client, experiment):
    sample = new_sample(experiment.id)
    new_session = random.randint(1, 1000)
    payload = {'session': new_session}
    response = client.put('/api/samples/%s' % sample.id, json=payload)
    assert response.status_code == 204
    updated = models.Samples.objects.get(id=sample.id)
    assert updated.session == new_session

    # test bad sample ID
    response = client.put('/api/samples/%s' % ObjectId(), json=payload)
    assert response.status_code == 404
    sample.delete()


def test_delete_sample(client, experiment):
    sample = new_sample(experiment.id)
    response = client.delete('/api/samples/%s' % sample.id)
    assert response.status_code == 204
    with pytest.raises(DoesNotExist):
        models.Samples.objects.get(id=sample.id)

    # test bad sample ID
    response = client.delete('/api/samples/%s' % sample.id)
    assert response.status_code == 404
    sample.delete()
