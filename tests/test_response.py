# coding:utf-8

import json
import pytest
from datetime import date, datetime
from mapletree import rsp, compat


def test_basics():
    class StartResponse(object):
        def __call__(self, status, headerlist):
            self.status = status
            self.headerlist = headerlist

    start_response = StartResponse()
    response = rsp().header('test', 1).code(404).body('abc')
    assert response(start_response) == [compat.non_unicode_str('abc')]
    assert start_response.status == '404 Not Found'
    assert start_response.headerlist == [('test', 1)]


def test_error():
    response = rsp()
    pytest.raises(rsp, response.error)


def test_location():
    response = rsp().location('abc')
    assert response._code == 301
    assert response._headers == {'Location': ['abc']}


def test_html():
    response = rsp().html('abc')
    assert response._headers['Content-Type'] == ['text/html']
    assert response._body == 'abc'


def test_json():
    response = rsp().json(datetime=datetime(1990, 1, 1, 1, 1, 1),
                          date=date(1990, 12, 31),
                          bytes=b'abcde',
                          set=set([1, 2, 3]))
    data = json.loads(response._body)
    assert response._headers['Content-Type'] == ['application/json']
    assert data['datetime'] == '1990/01/01 01:01:01'
    assert data['date'] == '1990/12/31'
    assert data['bytes'] == 'abcde'
    assert data['set'] == [1, 2, 3]


def test_json_error():
    pytest.raises(TypeError, rsp().json, key=object())
