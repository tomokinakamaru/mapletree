# coding:utf-8

import itertools
import pytest
from mapletree.routetree import RequestTree, ExceptionTree


methods = ['get', 'post', 'put', 'delete', 'head', 'options', 'patch']


@pytest.mark.parametrize('method, path',
                         itertools.product(methods,
                                           ['/test', '/test/test']))
def test_static_requesttree(path, method):
    rt = RequestTree()
    f = getattr(rt, method)

    @f(path)
    def _():
        return path

    item, pathinfo = rt.match(path)

    assert item[method]() == path
    assert pathinfo == {}


@pytest.mark.parametrize('method, path',
                         itertools.product(methods,
                                           ['/:test', '/test/:test']))
def test_dynamic_requesttree(path, method):
    rt = RequestTree()
    f = getattr(rt, method)

    @f(path)
    def _():
        return path

    item, pathinfo = rt.match(path.replace(':', ''))

    assert item[method]() == path
    assert pathinfo.get('test') == 'test'


def test_not_found():
    rt = RequestTree()

    @rt.get('/not_found')
    def _():
        return 100

    item, pathinfo = rt.match('/')

    assert item is None
    assert pathinfo == {}


@pytest.mark.parametrize('exc', [Exception, TypeError, ZeroDivisionError])
def test_exceptiontree(exc):
    et = ExceptionTree()

    @et(exc)
    def _():
        return exc.__name__

    item = et.match(exc)

    assert item() == exc.__name__


def test_non_strict():
    et = ExceptionTree()

    @et(Exception)
    def _():
        return 100

    item = et.match(TypeError)

    assert item() == 100


def test_requesttree_merge():
    rt1 = RequestTree()
    rt2 = RequestTree()

    @rt1.get('/test/test')
    def f1_1():
        pass

    @rt1.get('/test/test/')
    def f1_2():
        pass

    @rt2.get('/test/test/test1')
    def f2_1():
        pass

    @rt2.get('/test/:test/test2')
    def f2_2():
        pass

    rt1.merge(rt2)

    ret = []
    for key, item in rt1.items():
        ret.append((key, item))

    assert len(ret) == 4

    item, pathinfo = rt1.match('/test/test/test1')
    assert item['get'] == f2_1
    assert pathinfo == {}

    item, pathinfo = rt1.match('/test/x/test2')
    assert item['get'] == f2_2
    assert pathinfo.get('test') == 'x'


def test_exceptiontree_merge():
    et1, et2 = ExceptionTree(), ExceptionTree()

    @et1(Exception)
    def f1():
        pass

    @et2(TypeError)
    def f2():
        pass

    et1.merge(et2)
    assert len([(k, v) for k, v in et1.items()]) == 2
