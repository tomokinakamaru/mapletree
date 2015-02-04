# coding:utf-8

from .route import ExceptionRoute, RequestRoute
from .config import Config
from .wsgi import WSGIApp


class MapleTree(object):
    def __init__(self):
        self._exception_route = ExceptionRoute()
        self._request_route = RequestRoute()
        self._config = Config()

    def wsgiapp(self):
        return WSGIApp(self)

    @property
    def exception_route(self):
        return self._exception_route

    @property
    def request_route(self):
        return self._request_route

    @property
    def config(self):
        return self._config

    def exception(self, exc_cls):
        def _(f):
            self._exception_route.set(exc_cls, f)
            return f

        return _

    def request(self, rule, method):
        def _(f):
            self._request_route.setdefault(rule, {})[method] = f
            return f

        return _

    def get(self, rule):
        return self.request(rule, 'GET')

    def post(self, rule):
        return self.request(rule, 'POST')

    def put(self, rule):
        return self.request(rule, 'PUT')

    def delete(self, rule):
        return self.request(rule, 'DELETE')

    def patch(self, rule):
        return self.request(rule, 'PATCH')

    def head(self, rule):
        return self.request(rule, 'HEAD')

    def options(self, rule):
        return self.request(rule, 'OPTIONS')
