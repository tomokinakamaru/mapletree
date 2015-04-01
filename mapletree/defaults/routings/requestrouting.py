# coding:utf-8

from .routetree import RouteTree


class RequestRouting(object):
    def __init__(self):
        self._routetree = RouteTree()

    def __call__(self, environ):
        method = environ['REQUEST_METHOD']
        pathexpr = environ['PATH_INFO'] or '/'
        path = self._create_path(pathexpr)

        item, extra = self._routetree.get(path, True)

        if item is None:
            raise NotFound()

        if method not in item:
            raise MethodNotAllowed()

        return item[method], extra

    @property
    def routetree(self):
        return self._routetree

    def merge(self, request_routing):
        for path, item in request_routing.routetree:
            for method, f in item.items():
                self._routetree.set(path, {}, False).update({method: f})

    def route(self, method, pathexpr):
        def _route(f):
            path = self._create_path(pathexpr)
            self._routetree.set(path, {}, False).update({method: f})
            return f
        return _route

    def get(self, path):
        return self.route('GET', path)

    def post(self, path):
        return self.route('POST', path)

    def put(self, path):
        return self.route('PUT', path)

    def delete(self, path):
        return self.route('DELETE', path)

    def head(self, path):
        return self.route('HEAD', path)

    def options(self, path):
        return self.route('OPTIONS', path)

    def patch(self, path):
        return self.route('PATCH', path)

    def _create_path(self, pathexpr):
        return pathexpr.lstrip('/').split('/')


class RequestRoutingException(Exception):
    pass


class NotFound(RequestRoutingException):
    pass


class MethodNotAllowed(RequestRoutingException):
    pass
