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
"""Tests for the General Blueprint."""


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json.get('message') == 'success'


def test_login_logout(client, app):
    response = response = client.post('/login', data=dict(
        email=app.config['ADMIN_EMAIL'],
        password=app.config['ADMIN_PASSWORD']
    ), follow_redirects=True)
    assert response.status_code == 200
    # TODO: test correct page loads
    assert '</body>' in response.data

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    # TODO: test correct page loads
    assert '</body>' in response.data

    # TODO: bad username and bad password should have same failure message.

    # test bad login email
    response = response = client.post('/login', data=dict(
        email=app.config['ADMIN_EMAIL'],
        password='bad password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid password' in response.data

    # test bad login password
    response = response = client.post('/login', data=dict(
        email='invalidUser@me.com',
        password=app.config['ADMIN_PASSWORD']
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Specified user does not exist' in response.data


def test_secure(client, app):
    # test user creds
    email = app.config['ADMIN_EMAIL']
    password = app.config['ADMIN_PASSWORD']

    # test unauthenticated user is redirected to login page
    response = client.get('/secure')
    assert response.status_code == 302
    assert '/login?' in response.location

    # test successful login, redirected to /secure
    response = client.post(response.location, data=dict(
        email=email,
        password=password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert response.json.get('message') == 'success'


def test_admin(client, app):
    # test user creds
    email = app.config['ADMIN_EMAIL']
    password = app.config['ADMIN_PASSWORD']

    # test unauthenticated user is not allowed
    response = client.get('/admin')
    assert response.status_code == 403

    # test successful login, redirected to /secure
    response = client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)
    assert response.status_code == 200

    response = client.get('/admin')
    assert response.status_code == 200
    assert response.json.get('message') == 'success'


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # TODO: test HTML response?
    assert '</body>' in response.data
