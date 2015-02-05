# coding:utf-8


class RouteFunc(object):
    def __init__(self, *args):
        self._args = args

    def __call__(self, f):
        self._f = f
        return self

    def __get__(self, reusable, c=None):
        def _(*args, **kwargs):
            return self._f(reusable, *args, **kwargs)

        reusable.routes[self._args] = _
        return _
