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

import random

import pytest
from mongoengine import connect, disconnect

from deepcell_datasets.database import models


@pytest.fixture()
def mongodb():
    disconnect()  # TODO: why do we need to call this?
    db = connect('mongoenginetest', host='mongomock://localhost')
    yield db
    disconnect()


@pytest.fixture()
def sample(mongodb):
    session = random.randint(1, 9999)
    position = random.randint(1, 9999)

    sample = models.Samples(session=session, position=position)

    sample.save()
    yield sample

    sample.delete()


@pytest.fixture()
def experiment(mongodb):
    doi = 'a specific DOI number'
    created_by = models.Users(
        first_name='first',
        last_name='last',
        facility='test facility'
    )
    created_by.save()

    experiment = models.Experiments(doi=doi, created_by=created_by)
    experiment.save()
    yield experiment

    experiment.delete()


class TestExperiments(object):

    def test_create(self, mongodb):
        doi = 'a specific DOI number'
        created_by = models.Users(
            first_name='first',
            last_name='last',
            facility='test facility'
        )
        created_by.save()
        exp = models.Experiments(doi=doi, created_by=created_by)
        exp.save()

        fresh_experiment = models.Experiments.objects(id=exp.id).first()
        assert fresh_experiment is not None
        assert fresh_experiment.doi == doi
        assert fresh_experiment.created_by == created_by
        assert fresh_experiment.id == exp.id

    def test_update(self, experiment):
        new_doi = 'new doi value'
        experiment.update(doi=new_doi)
        updated_experiment = models.Experiments.objects(id=experiment.id).first()

        assert updated_experiment.id == experiment.id
        assert updated_experiment.created_by == experiment.created_by
        assert updated_experiment.doi == new_doi

    def test_delete(self, experiment):
        experiment.delete()
        no_experiment = models.Experiments.objects(id=experiment.id).first()
        assert no_experiment is None

    def test_remove_sample(self, experiment, sample):
        sample.update(experiment=experiment)

        updated_experiment = models.Experiments.objects(id=experiment.id).first()

        # can find sample based on experiment ID.
        updated_sample = models.Samples.objects(experiment=experiment.id).first()
        assert updated_sample.experiment.id == updated_experiment.id

        # now delete the sample, experiment should exist but not have the sample
        updated_sample.delete()
        updated_experiment = models.Experiments.objects(id=experiment.id).first()
        assert updated_experiment.id == experiment.id

        updated_sample = models.Samples.objects(experiment=experiment.id).first()
        assert updated_sample is None


class TestSamples(object):

    def test_create(self, mongodb):
        session = random.randint(1, 99)
        position = random.randint(1, 99)

        sample = models.Samples(session=session, position=position)
        sample.save()

        fresh_sample = models.Samples.objects(id=sample.id).first()
        assert fresh_sample is not None
        assert fresh_sample.session == session
        assert fresh_sample.position == position

    def test_update(self, sample):
        session = random.randint(1, 9999)

        sample.update(session=session)

        updated_sample = models.Samples.objects(id=sample.id).first()
        assert updated_sample.id == sample.id
        assert updated_sample.position == sample.position
        assert updated_sample.session == session

    def test_delete(self, sample):
        sample.delete()
        no_sample = models.Samples.objects(id=sample.id).first()
        assert no_sample is None

    def test_add_experiment(self, experiment, sample):
        sample.update(experiment=experiment.id)

        updated_sample = models.Samples.objects(id=sample.id).first()
        assert updated_sample.id == sample.id
        assert updated_sample.experiment.id == experiment.id

        updated_sample = models.Samples.objects(experiment=experiment.id).first()
        assert updated_sample.id == sample.id
        assert updated_sample.experiment.id == experiment.id

        # remove the experiment, the sample.experiment should be None
        experiment.delete()
        updated_sample = models.Samples.objects(id=sample.id).first()
        # using NULLIFY so the sample will still exist.
        assert updated_sample.id == sample.id
        assert updated_sample.experiment is None
