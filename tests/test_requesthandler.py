# coding:utf-8

import pytest
from mapletree.requesthandler import (RequestHandler,
                                      NotFound,
                                      MethodNotAllowed)


@pytest.mark.parametrize('method', ['get', 'post', 'put', 'delete',
                                    'head', 'options', 'patch'])
def test_basics(method):
    rr = RequestHandler()
    f = getattr(rr, method)

    @f('/')
    def endpoint():
        pass

    environ = {'REQUEST_METHOD': method.upper(), 'PATH_INFO': '/'}
    assert rr(environ) == (endpoint, {})


def test_not_found():
    rr = RequestHandler()
    environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
    pytest.raises(NotFound, rr, environ)


def test_method_not_allowed():
    rr = RequestHandler()

    @rr.post('/')
    def endpoint():
        pass

    environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
    pytest.raises(MethodNotAllowed, rr, environ)


def test_merge():
    rr1, rr2 = RequestHandler(), RequestHandler()

    @rr1.get('/')
    def endpoint1():
        pass

    @rr2.post('/')
    def endpoint2():
        pass

    @rr2.put('/:a')
    def endpoint3():
        pass

    rr1.merge(rr2)

    environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
    assert rr1(environ) == (endpoint1, {})
    environ = {'REQUEST_METHOD': 'POST', 'PATH_INFO': '/'}
    assert rr1(environ) == (endpoint2, {})
    environ = {'REQUEST_METHOD': 'PUT', 'PATH_INFO': '/x'}
    assert rr1(environ) == (endpoint3, {'a': 'x'})
