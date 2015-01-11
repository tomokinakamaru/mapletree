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

    def __call__(self):
        return self._code, self._headers, self._body

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
