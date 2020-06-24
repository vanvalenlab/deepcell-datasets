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
"""Tests for the Flask application."""

from mongoengine import disconnect

import pytest

from deepcell_datasets import create_app


def test_config(monkeypatch):
    monkeypatch.setenv('MONGODB_USERNAME', 'testUser')
    monkeypatch.setenv('MONGODB_PASSWORD', 'testPwd')

    assert not create_app().testing
    # Without calling disconnect(), we hit a ConnectionFailure:
    # A different connection with alias `default` was  already registered.
    # Use disconnect() first.
    disconnect()  # TODO: how can we remove this?
    assert create_app(TESTING=True).testing