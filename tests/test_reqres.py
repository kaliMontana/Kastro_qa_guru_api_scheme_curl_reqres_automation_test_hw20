import logging

import requests
from jsonschema.validators import validate

from helper import reqres_session, load_json_schema

path_users = '/api/users'
path_register = '/api/register'
path_login = '/api/login'


def test_page_number():
    page = 1

    response = reqres_session.get(path_users, params={'page': page})

    logging.info(response.json())

    assert response.status_code == 200


def test_length_data_response():
    page = 1
    length = 3

    response = reqres_session.get(path_users, params={'page': page, 'per_page': length})

    assert len(response.json()['data']) == length


def test_single_user():
    query = '/8'

    response = reqres_session.get(f'{path_users}{query}')

    assert response.status_code == 200
    assert response.json()['data']['id'] == 8
    assert response.json()['data']['email'] == 'lindsay.ferguson@reqres.in'
    assert response.json()['data']['first_name'] == 'Lindsay'
    assert response.json()['data']['last_name'] == 'Ferguson'


def test_single_user_no_found():
    query = '/18'

    response = reqres_session.get(f'{path_users}{query}')

    assert response.status_code == 404
    assert response.json() == {}


def test_create():
    name = 'Dania'
    job = 'Pilot'
    schema = load_json_schema('post_create_user.json')

    response = reqres_session.post(
        url=f'{path_users}',
        json={
            'name': name,
            'job': job
        }
    )

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_patch():
    query = '/8'
    name = 'Ximena'
    job = 'accountant'

    response = reqres_session.patch(
        url=f'{path_users}{query}',
        json={
            'name': name,
            'job': job
        }
    )

    assert response.status_code == 200
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_delete():
    query = '/8'

    response = reqres_session.delete(url=f'{path_users}{query}')

    assert response.status_code == 204
    assert response.text == ''


def test_register_successful():
    email = 'emma.wong@reqres.in'
    password = '12345'
    id = 3
    token = 'QpwL5tke4Pnpja7X3'

    response = reqres_session.post(
        url=f'{path_register}',
        json={
            'email': email,
            'password': password
        }
    )

    assert response.status_code == 200
    assert response.json()['id'] == id
    assert response.json()['token'] == token


def test_register_unsuccessful():
    email = 'emma.wong@reqres.in'
    error_message = 'Missing password'

    response = reqres_session.post(
        url=f'{path_register}',
        json={
            'email': email
        }
    )

    assert response.status_code == 400
    assert response.status_code == requests.codes.bad_request
    assert response.json()['error'] == error_message


def test_login_successful():
    email = 'emma.wong@reqres.in'
    password = 'cyg123'
    token = 'QpwL5tke4Pnpja7X3'

    response = reqres_session.post(
        url=f'{path_login}',
        json={
            'email': email,
            'password': password
        }
    )

    assert response.status_code == requests.codes.ok
    assert response.json()['token'] == token
