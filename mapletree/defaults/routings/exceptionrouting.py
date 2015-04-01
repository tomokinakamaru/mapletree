# coding:utf-8

from .routetree import RouteTree


class ExceptionRouting(object):
    def __init__(self):
        self._routetree = RouteTree()

    def __call__(self, exc):
        path = self._create_path(exc.__class__)
        f, _ = self._routetree.get(path, False)

        if f is None:
            raise NoExceptionHandler()

        return f

    @property
    def routetree(self):
        return self._routetree

    def merge(self, exception_routing):
        for path, f in exception_routing.routetree:
            self._routetree.set(path, f, True)

    def route(self, exc_cls):
        def _route(f):
            path = self._create_path(exc_cls)
            self._routetree.set(path, f, True)
            return f
        return _route

    def _create_path(self, exc_cls):
        if exc_cls is Exception:
            return []

        else:
            super_cls = exc_cls.__bases__[0]
            return self._create_path(super_cls) + [exc_cls.__name__]


class ExceptionRoutingException(Exception):
    pass


class NoExceptionHandler(ExceptionRoutingException):
    pass
