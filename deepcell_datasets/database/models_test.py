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
"""Tests for the Mongo Models."""

import pytest
from mongoengine import connect, disconnect

from deepcell_datasets.database import models


@pytest.fixture()
def mongodb():
    disconnect()  # TODO: why do we need to call this?
    db = connect('mongoenginetest', host='mongomock://localhost')
    yield db
    disconnect()


# TODO: test adding Session to an Experiment.


def test_experiments(mongodb):
    # test create
    doi = 'a specific DOI number'
    created_by = models.Users(
        first_name='first',
        last_name='last',
        facility='test facility'
    )
    created_by.save()

    experiment = models.Experiments(doi=doi, created_by=created_by)
    experiment.save()

    # test read
    fresh_experiment = models.Experiments.objects().first()
    assert fresh_experiment is not None
    assert fresh_experiment.doi == doi
    assert fresh_experiment.created_by == created_by

    # test update
    new_doi = 'new doi value'
    fresh_experiment.update(doi=new_doi)
    updated_experiment = models.Experiments.objects().first()

    assert updated_experiment.id == fresh_experiment.id
    assert updated_experiment.created_by == fresh_experiment.created_by
    assert updated_experiment.doi == new_doi

    # test delete
    updated_experiment.delete()
    no_experiment = models.Experiments.objects().first()
    assert no_experiment is None


def test_samples(mongodb):
    # test create
    session = 1
    position = 99

    sample = models.Samples(session=session, position=position)
    sample.save()

    # test read
    fresh_sample = models.Samples.objects().first()
    assert fresh_sample is not None
    assert fresh_sample.session == session
    assert fresh_sample.position == position

    # test update
    new_session = session + 1
    fresh_sample.update(session=new_session)
    updated_sample = models.Samples.objects().first()

    assert updated_sample.id == fresh_sample.id
    assert updated_sample.position == fresh_sample.position
    assert updated_sample.session == new_session

    # test delete
    updated_sample.delete()
    no_sample = models.Samples.objects().first()
    assert no_sample is None
