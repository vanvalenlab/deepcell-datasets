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
"""Initialization Script for DeepCell Datasets Database"""

# This script should run when the Database is first brought online.
# It should traverse a given directory, locate metadata files, and import
# the information it finds into the relevant collection.

import os
import re


def sorted_nicely(list_to_sort):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list_to_sort, key=alphanum_key)


def _datasets_available(self):
    # This function should be part of a different system and constantly maintained
    # This is a placeholder for a database that tells us what data is available
    for (cur_dir, sub_dirs, files) in os.walk(self.base_path):
        if not sub_dirs and not files:
            print(cur_dir)
            print('empty directory')
            print('--------------------------------')
        if not sub_dirs and len(files) == 2:
            print(cur_dir)
            print('only 1 file')
            print('--------------------------------')


def csv_loader():
    """Load Greenwald et al multiplex data using pandas and provided xlsx"""
