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


class TestSpecimen(object):

    def test_create_specimen(self, mongodb):
        spec_id = ['cell', 'HEK293']
        ontology_loc = ['dynamic', '2d']
        num_frames = 10
        specimen = models.Specimen(
            spec_id=spec_id,
            ontology_loc=ontology_loc,
            # num_frames=num_frames,
            # exp_id='schema',
        )
        specimen.save()

        fresh_specimen = models.Specimen.objects().first()
        assert fresh_specimen is not None
        assert fresh_specimen.spec_id == spec_id
        assert fresh_specimen.ontology_loc == ontology_loc


# class TestDynamicSpecimen(object):
#
#     def test_create_dynamic_specimen(self, mongodb):
#         spec_type = ['cell', 'HEK293']
#         ontology_loc = ['dynamic', '2d']
#         num_frames = 10
#         time_step = 'this is a time step?'
#         specimen = models.DynamicSpecimen(
#             spec_type=spec_type,
#             ontology_loc=ontology_loc,
#             num_frames=num_frames,
#             time_step=time_step,
#         )
#         specimen.save()
#
#         fresh_specimen = models.DynamicSpecimen.objects().first()
#         assert fresh_specimen.spec_type == spec_type
#         assert fresh_specimen.ontology_loc == ontology_loc
#         assert fresh_specimen.num_frames == num_frames
#         assert fresh_specimen.time_step == time_step
#
#
# class TestThreeDimSpecimen(object):
#
#     def test_create_dynamic_specimen(self, mongodb):
#         spec_type = ['cell', 'HEK293']
#         ontology_loc = ['static', '3d']
#         num_frames = 10
#         z_step = 'this is a z step?'
#         specimen = models.ThreeDimSpecimen(
#             spec_type=spec_type,
#             ontology_loc=ontology_loc,
#             num_frames=num_frames,
#             z_step=z_step,
#         )
#         specimen.save()
#
#         fresh_specimen = models.ThreeDimSpecimen.objects().first()
#         assert fresh_specimen.spec_type == spec_type
#         assert fresh_specimen.ontology_loc == ontology_loc
#         assert fresh_specimen.num_frames == num_frames
#         assert fresh_specimen.z_step == z_step
