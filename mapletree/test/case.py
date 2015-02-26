# coding:utf-8

import copy
import mimetypes
import random
import sys
import urllib
from json import dumps as jsonencode
from mimetypes import guess_type as mimetype_of
from StringIO import StringIO
from wsgiref.util import setup_testing_defaults
from .result import Result
from .startresponse import StartResponse


class Case(object):
    def __init__(self, environ={}):
        self._environ = {}
        self._environ.update(environ)

    def run(self, app):
        env = self.copy_environ()
        env.setdefault('wsgi.errors', sys.stdout)
        env.setdefault('QUERY_STRING', '')
        env.setdefault('CONTENT_TYPE', '')
        env.setdefault('CONTENT_LENGTH', 0)
        setup_testing_defaults(env)
        start_response = StartResponse()
        body = app(env, start_response)
        return Result(body, start_response)

    def copy_environ(self):
        return copy.deepcopy(self._environ)

    def copy(self):
        return Case(self.copy_environ())

    def environ(self, k, v):
        self._environ[k] = v
        return self

    def http_header(self, k, v):
        return self.environ('HTTP_' + k.upper(), v)

    def method(self, m):
        return self.environ('REQUEST_METHOD', m.upper())

    def get(self):
        return self.method('get')

    def post(self):
        return self.method('post')

    def put(self):
        return self.method('put')

    def delete(self):
        return self.method('delete')

    def patch(self):
        return self.method('patch')

    def head(self):
        return self.method('head')

    def options(self):
        return self.method('options')

    def path(self, p):
        return self.environ('PATH_INFO', p)

    def ctype(self, t):
        return self.environ('CONTENT_TYPE', t)

    def clength(self, l):
        return self.environ('CONTENT_LENGTH', str(l))

    def params(self, **kwargs):
        return self.environ('QUERY_STRING', urllib.urlencode(kwargs))

    def cookie(self, **kwargs):
        return self.http_header('cookie', urllib.urlencode(kwargs))

    def body(self, b):
        io = StringIO(b)
        return self.environ('wsgi.input', io).clength(io.len)

    def data(self, **kwargs):
        boundary = '----------boundarywsgitest' + str(random.random())

        content_disposition = 'Content-Disposition: form-data; name="{}"'
        f_content_disposition = content_disposition + '  filename="{}"'
        f_content_type = 'Content-Type: {}'

        lines = []
        for k, v in kwargs.items():
            lines.append('--' + boundary)
            if isinstance(v, file):
                lines.append(f_content_disposition.format(k))
                lines.append(f_content_type.format(mimetype_of(v.name)))
                lines.append('')
                lines.append(v.read())

            else:
                lines.append(content_disposition.format(k))
                lines.append('')
                lines.append(str(v))

        lines.append('--' + boundary + '--')
        lines.append('')

        ctype = 'multipart/form-data; boundary={}'.format(boundary)
        return self.ctype(ctype).body('\r\n'.join(lines))

    def json(self, **kwargs):
        return self.ctype('text/plain').body(jsonencode(kwargs))

    def __str__(self):
        m = self._environ['REQUEST_METHOD']
        p = self._environ['PATH_INFO']
        return '{} {}'.format(m, p)
