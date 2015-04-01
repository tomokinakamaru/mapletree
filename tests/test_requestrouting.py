# coding:utf-8

import pytest
from mapletree.defaults.routings import (RequestRouting,
                                         NotFound,
                                         MethodNotAllowed)


@pytest.mark.parametrize('method', ['get', 'post', 'put', 'delete',
                                    'head', 'options', 'patch'])
def test_basics(method):
    rr = RequestRouting()
    f = getattr(rr, method)

    @f('/')
    def endpoint():
        pass

    environ = {'REQUEST_METHOD': method.upper(), 'PATH_INFO': '/'}
    assert rr(environ) == (endpoint, {})


def test_not_found():
    rr = RequestRouting()
    environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
    pytest.raises(NotFound, rr, environ)


def test_method_not_allowed():
    rr = RequestRouting()

    @rr.post('/')
    def endpoint():
        pass

    environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
    pytest.raises(MethodNotAllowed, rr, environ)


def test_merge():
    rr1, rr2 = RequestRouting(), RequestRouting()

    @rr1.get('/')
    def endpoint1():
        pass

    @rr2.post('/')
    def endpoint2():
        pass

    rr1.merge(rr2)

    environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
    assert rr1(environ) == (endpoint1, {})
    environ = {'REQUEST_METHOD': 'POST', 'PATH_INFO': '/'}
    assert rr1(environ) == (endpoint2, {})
