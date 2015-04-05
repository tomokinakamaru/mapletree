# coding:utf-8

import requests
from app.app import mt, Client

mt.build()
mt.run(background=True)


def test_basics():
    c = Client()
    assert c('get', '/').status_code == 200


def test_not_found():
    c = Client()
    assert c('get', '/not_found').status_code == 404


def test_cookie():
    c = Client()
    assert c('get', '/set_cookie').status_code == 200

    r = c('get', '/use_cookie')
    assert r.json()['cookie'] == {'cookie': '100'}

    r = c('get', '/clear_cookie')
    r = c('get', '/use_cookie')
    assert r.json()['cookie'] == {}


def test_params():
    c = Client()
    params = {'a': '100'}
    assert c('get', '/params', params=params).json() == params


def test_data():
    c = Client()
    data = {'a': 'abcdefg'}
    assert c('post', '/data', data=data).json() == data


def test_read_twice():
    c = Client()
    assert c('post', '/read_twice1').status_code == 500
    assert c('post', '/read_twice2').status_code == 500


def test_extra():
    c = Client()
    assert c('get', '/extra/abc').json() == {'label': 'abc'}


def test_files():
    c = Client()
    with open('README.rst') as readme, open('LICENSE') as license:
        r = c('post', '/files', files={'f1': readme, 'f2': license})
        assert r.status_code == 200
        assert r.json() == {'f1': 'README.rst', 'f2': 'LICENSE'}
