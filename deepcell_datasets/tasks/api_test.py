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
"""Tests for the Task Blueprint."""

import random

import pytest
from mongoengine import DoesNotExist

from deepcell_datasets.database import models


def new_task(annotation_id):
    """Create new task with some static values"""
    # Defined required fields
    session = 1
    position = 2
    spatial_dim = random.choice(['2d', '3d'])
    kinetics = random.choice(['static', 'dynamic'])

    # Create the task
    task = models.Tasks(
        session=session,
        position=position,
        spatial_dim=spatial_dim,
        kinetics=kinetics,
        annotation=annotation_id,
    )
    task.save()
    return task


def test_get_all_task(client, annotation):
    # database should be empty
    response = client.get('/api/tasks/')
    assert response.status_code == 200
    assert response.json == []

    # create new task get all again.
    task = new_task(annotation.id)
    response = client.get('/api/tasks/')
    assert len(response.json) == 1
    assert response.json[0]['session'] == task.session
    assert response.json[0]['position'] == task.position
    task.delete()


def test_get_task(client, annotation):
    task = new_task(annotation.id)
    response = client.get('/api/tasks/%s' % task.id)
    assert response.status_code == 200
    assert response.json['session'] == task.session
    assert response.json['position'] == task.position

    # test bad task ID
    response = client.get('/api/tasks/%s' % 5)
    assert response.status_code == 404
    task.delete()


def test_create_task(client, annotation):
    session = random.randint(1, 1000)
    position = random.randint(1, 1000)
    spatial_dim = random.choice(['2d', '3d'])
    kinetics = random.choice(['static', 'dynamic'])
    body = {
        'session': session,
        'position': position,
        'spatial_dim': spatial_dim,
        'kinetics': kinetics,
        'annotation': str(annotation.id),
    }
    response = client.post('/api/tasks/', json=body)
    assert response.status_code == 200
    unique_id = response.json['unique_id']
    assert unique_id is not None
    # test that the ID exists in the database
    task = models.Tasks.objects.get(id=unique_id)
    assert task.session == session
    assert task.position == position
    assert str(task.id) == str(unique_id)
    # test bad body payload
    bad_body = {'session': 0}
    response = client.post('/api/tasks/', json=bad_body)
    assert response.status_code == 400


def test_update_task(client, annotation):
    task = new_task(annotation.id)
    new_session = random.randint(1, 1000)
    payload = {'session': new_session}
    response = client.put('/api/tasks/%s' % task.id, json=payload)
    assert response.status_code == 204
    updated = models.Tasks.objects.get(id=task.id)
    assert updated.session == new_session

    # test bad task ID
    response = client.put('/api/tasks/%s' % 1, json=payload)
    assert response.status_code == 404
    task.delete()


def test_delete_task(client, annotation):
    task = new_task(annotation.id)
    response = client.delete('/api/tasks/%s' % task.id)
    assert response.status_code == 204
    with pytest.raises(DoesNotExist):
        models.Tasks.objects.get(id=task.id)

    # test bad task ID
    response = client.delete('/api/tasks/%s' % task.id)
    assert response.status_code == 404
    task.delete()
