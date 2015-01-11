# coding:utf-8

import sys
from .httpio import Request, Response
from .exceptions import InvalidStatusCode, NotFound, MethodNotAllowed


class WSGIApp(object):
    def __init__(self, mapletree):
        self.request_route = mapletree.request_route
        self.exception_route = mapletree.exception_route

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            sys.stdout = request.environ('wsgi.errors')
            sys.stderr = request.environ('wsgi.errors')

            response = self._handle_request(request)
            return http_response(start_response, response)

        except Exception as exception:
            response = self._handle_exception(exception)
            return http_response(start_response, response)

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


def http_response(start_response, response):
    code, headers, body = response()

    status = http_status(code)
    headerlist = http_headers(headers)

    start_response(status, headerlist)
    return [body]


def http_status(code):
    if code in RESPONSE_STATUS_PHRASES:
        return str(code) + ' ' + RESPONSE_STATUS_PHRASES[code]

    else:
        raise InvalidStatusCode(code)


def http_headers(headerdict):
    headerlist = []
    for k, ls in headerdict.items():
        for e in ls:
            headerlist.append((k, e))

    return headerlist


RESPONSE_STATUS_PHRASES = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Moved Temporarily",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Time-out",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Large",
    415: "Unsupported Media Type",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version not supported"
}
