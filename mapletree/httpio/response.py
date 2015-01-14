# coding:utf-8

import json
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
from .session import Session


class Response(Exception):
    def __init__(self):
        self._code = 200
        self._headers = {}
        self._body = ''

    def __call__(self, start_response):
        status = str(self._code) + ' ' + STATUS_PHRASES[self._code]

        headerlist = []
        for k, ls in self._headers.items():
            for e in ls:
                headerlist.append((k, e))

        start_response(status, headerlist)
        return [self._body]

    def error(self):
        raise self

    def code(self, c):
        self._code = c
        return self

    def header(self, k, v, replace=True):
        if replace:
            self._headers[k] = [v]

        else:
            self._headers.setdefault(k, []).append(v)

        return self

    def body(self, b):
        self._body = b
        return self

    def ctype(self, t):
        return self.header('Content-Type', t)

    def location(self, l):
        return self.code(301).header('Location', l)

    def cookie(self, k, v, expires=None, domain=None, path='/', secure=False):
        ls = ['{}={}'.format(k, v)]

        if expires is not None:
            ls.append('expires={}'.format(httpdate(expires)))

        if domain is not None:
            ls.append('domain={}'.format(domain))

        if path is not None:
            ls.append('path={}'.format(path))

        if secure:
            ls.append('secure')

        return self.header('Set-Cookie', '; '.join(ls), False)

    def clear_cookie(self, k):
        return self.cookie(k, '', datetime.fromtimestamp(0))

    def session(self, data, expires=None, domain=None, path='/', secure=False):
        return self.cookie(
            Session.COOKIE_NAME,
            Session(data).encode(),
            expires,
            domain,
            path,
            secure
        )

    def clear_session(self):
        return self.clear_cookie(Session.COOKIE_NAME)

    def json(self, **kwargs):
        return self.ctype('application/json').body(jsonencode(kwargs))

    def html(self, b):
        return self.ctype('text/html').body(b)


def jsonencode(obj):
    return json.dumps(obj, separators=(',', ':'), default=jsondefault)


def jsondefault(obj):
    if isinstance(obj, datetime):
        return httpdate(obj)

    if isinstance(obj, bytearray):
        return str(obj)

    return json.JSONEncoder.default(obj)


def httpdate(dt):
    return format_date_time(mktime(dt.timetuple()))


STATUS_PHRASES = {
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
