# coding:utf-8

from mapletree.defaults.routings.routetree import RouteTree


def test_basics():
    rt = RouteTree()
    rt.set(['a', 'b'], 100, True)
    assert rt.get(['a', 'b'], True) == (100, {})


def test_wildcard():
    rt = RouteTree()
    rt.set(['c', ':d'], 200, True)
    assert rt.get(['c', 'x'], True) == (200, {'d': 'x'})


def test_non_strict():
    rt = RouteTree()
    rt.set(['a', 'b'], 100, True)
    assert rt.get(['a', 'b', 'c'], False) == (100, {})


def test_non_existance():
    rt = RouteTree()
    rt.set(['a'], 200, True)
    assert rt.get(['b'], True) == (None, {})


def test_iter():
    rt = RouteTree()
    rt.set(['a'], 'a', True)
    for path, item in rt:
        assert path[0] == item


def test_iter_wildcard():
    rt = RouteTree()
    rt.set([':c'], 100, True)
    for path, item in rt:
        assert path == [':c']
        assert item == 100
