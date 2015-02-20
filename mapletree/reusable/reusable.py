# coding:utf-8

from .routefunc import RouteFunc


class Reusable(object):
    ROUTE_METHOD_PREFIX = 'route_'

    def __init__(self):
        self.debug = False
        self._routes = {}

    def __call__(self, router, prefix=''):
        for k in dir(self):
            if k.startswith(self.ROUTE_METHOD_PREFIX):
                getattr(self, k)

        for k, f in self._routes.items():
            if len(k) == 2:
                method, path = k
                getattr(router, method)(prefix + path)(f)

            elif len(k) == 1:
                exc_cls = k[0]
                getattr(router, 'exception')(exc_cls)(f)

    @property
    def routes(self):
        return self._routes

    @classmethod
    def exception(cls, exc_cls):
        return RouteFunc(exc_cls)

    @classmethod
    def request(cls, method, path):
        return RouteFunc(method, path)

    @classmethod
    def get(cls, path):
        return RouteFunc('get', path)

    @classmethod
    def post(cls, path):
        return RouteFunc('post', path)

    @classmethod
    def put(cls, path):
        return RouteFunc('put', path)

    @classmethod
    def delete(cls, path):
        return RouteFunc('delete', path)

    @classmethod
    def head(cls, path):
        return RouteFunc('head', path)

    @classmethod
    def options(cls, path):
        return RouteFunc('options', path)

    @classmethod
    def patch(cls, path):
        return RouteFunc('patch', path)
