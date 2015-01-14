# coding:utf-8

import sys
from .driver import run
from .httpio import Request, Response
from .exceptions import NotFound, MethodNotAllowed


class WSGIApp(object):
    def __init__(self, mapletree):
        self.request_route = mapletree.request_route
        self.exception_route = mapletree.exception_route

    def run(self, host='localhost', port=5000):
        run(self, host=host, port=port)

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            sys.stdout = request.environ('wsgi.errors')
            sys.stderr = request.environ('wsgi.errors')

            response = self._handle_request(request)
            return response(start_response)

        except Exception as exception:
            response = self._handle_exception(exception)
            return response(start_response)

    def _handle_request(self, request):
        try:
            item, info = self.request_route.get(request.path)

            if item is None:
                raise NotFound(request.method, request.path)

            if request.method not in item:
                raise MethodNotAllowed(request.method, request.path)

            request.pathparams.update(info)
            return item[request.method](request)

        except Response as response:
            return response

    def _handle_exception(self, exception):
        item = self.exception_route.get(exception.__class__)

        if item is None:
            fmt = 'No exception handler found for {}'
            raise Exception(fmt.format(exception.__class__))

        return item(exception)
