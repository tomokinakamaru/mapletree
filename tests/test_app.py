# coding:utf-8

import json
import pytest
import requests
import time
from test_app_pkg.app import mt

mt.run(background=True)


def test_run():
    mt.run()


@pytest.mark.parametrize('method',
                         ['get', 'post', 'put', 'delete',
                          'options', 'head', 'patch'])
def test_basic(method):
    r = requests.request(method, 'http://localhost:5000')
    assert r.status_code == 200


def test_not_found():
    r = requests.get('http://localhost:5000/not_found')
    assert r.status_code == 404


def test_method_not_allowd():
    r = requests.post('http://localhost:5000/get_only')
    assert r.status_code == 405


def test_response_error():
    r = requests.get('http://localhost:5000/error')
    assert r.status_code == 500


def test_unhandled_error():
    r = requests.get('http://localhost:5000/unhandled_error')
    assert r.status_code == 500


@pytest.mark.parametrize('params',
                         [{'x': '1'},
                          {'x': '100', 'y': '200'}])
def test_params(params):
    r = requests.get('http://localhost:5000/params', params=params)
    assert r.status_code == 200
    assert r.json() == params


@pytest.mark.parametrize('data',
                         [{'x': 'texttext'},
                          {'x': 'text', 'y': 'text'}])
def test_data(data):
    r = requests.post('http://localhost:5000/data', data=data)
    assert r.status_code == 200
    assert r.json() == data


@pytest.mark.parametrize('fname',
                         ['AUTHORS'])
def test_file_uploads(fname):
    r = requests.post('http://localhost:5000/files',
                      files={'f': open(fname, 'rb')})
    assert r.status_code == 200


def test_read_body():
    r = requests.post('http://localhost:5000/readbody1')
    assert r.status_code == 500

    r = requests.post('http://localhost:5000/readbody2')
    assert r.status_code == 500


def test_cookie():
    s = requests.Session()
    r = s.post('http://localhost:5000/setcookie')
    assert r.status_code == 200

    r = s.get('http://localhost:5000/usecookie')
    assert r.status_code == 200
    assert r.json() == {'a': '1'}

    r = s.get('http://localhost:5000/clearcookie')
    assert r.status_code == 200

    r = s.get('http://localhost:5000/usecookie')
    assert r.status_code == 200
    assert r.json() == {}


def test_https_cookie():
    s = requests.Session()
    r = s.post('http://localhost:5000/httpscookie')
    assert r.status_code == 200

    r = s.get('http://localhost:5000/usecookie')
    assert r.status_code == 200
    assert r.json() == {}


def test_domain_cookie():
    s = requests.Session()
    r = s.post('http://localhost:5000/domaincookie')
    assert r.status_code == 200

    r = s.get('http://localhost:5000/usecookie')
    assert r.status_code == 200
    assert r.json() == {}


@pytest.mark.parametrize('data',
                         [{'x': 'texttext'},
                          {'x': 'text', 'y': 'text'}])
def test_json(data):
    r = requests.post('http://localhost:5000/json',
                      data=json.dumps(data),
                      headers={'Content-type': 'application/json'})
    assert r.status_code == 200
    assert r.json() == data


def test_bad_json():
    r = requests.post('http://localhost:5000/json', data='aaa:a')
    assert r.status_code == 500


def test_html():
    r = requests.get('http://localhost:5000/html', params={'a': 1})
    assert r.status_code == 200
    assert r.text == '<html>{}</html>'.format(1)


def test_location():
    r = requests.get('http://localhost:5000/location')
    assert r.status_code == 200


def test_jsonencode():
    r = requests.get('http://localhost:5000/jsonencode')
    assert r.status_code == 200
    assert r.json()['set'] == [1, 2, 3]


def test_not_json_serializable():
    r = requests.get('http://localhost:5000/not_json_serializable')
    assert r.status_code == 500
