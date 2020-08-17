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
"""Utility functions"""


def nest_dict(flat_dict, sep='-'):
    """Return nested dict by splitting the keys on a delimiter.

    Flask-wtf returns embedded document fields as a flattened dict, with
    embedded document names embedded in the key. Any keys with empty values
    will be removed.

    For example, a document User may have an embedded document Comment.
    Flask-wtf will return this in a form as "user-comment". This function
    returns a nested dictionary like d["user"]["comment"].

    Args:
        flat_dict (dict): Flattened dict of embedded document fields.
        sep (str): Seperator between nested keys.

    Returns:
        dict: Nested dictionary which better represents the embedded documents.
    """

    # Start a new dict to hold top level keys and take values for these top level keys
    new_dict = {}
    hyphen_dict = {}
    eds = set()
    for k, v in flat_dict.items():
        if not v:
            pass
        elif '-' not in k:
            new_dict[k] = v
        else:
            hyphen_dict[k] = v
            eds.add(k.split(sep)[0])

    # Create a new nested dict for each embedded document
    # And add these dicts to the correct top level key
    ed_dict = {}
    for ed in eds:
        ed_dict = {}
        for k, v in hyphen_dict.items():
            if ed == k.split(sep)[0]:
                ed_dict[k.split(sep)[1]] = v
        new_dict[ed] = ed_dict

    return new_dict
