# coding:utf-8

import cgi
import copy
import datetime
import json
import re
from xml.dom.minidom import parseString as xmldecode
from . import compat
from .exceptions import (ValidationError,
                         InsufficientError,
                         ReadBodyTwiceError)


class Request(object):
    def __init__(self, environ):
        self._environ = environ
        self._body = None
        self._fieldstorage = None
        self._params = None
        self._cookie = None
        self._data = None
        self._json = None
        self._pathparams = None

    @classmethod
    def validator(cls, f):
        return VDict.validator(f)

    def environ(self, key):
        return self._environ.get(key)

    def http_header(self, name):
        return self._environ.get('HTTP_' + name.upper())

    @property
    def method(self):
        return self._environ.get('REQUEST_METHOD')

    @property
    def path(self):
        return self._environ.get('PATH_INFO') or '/'

    @property
    def query(self):
        return self._environ.get('QUERY_STRING')

    @property
    def body(self):
        if self._body is None:
            if self._fieldstorage is not None:
                raise ReadBodyTwiceError()

            clength = int(self.environ('CONTENT_LENGTH') or 0)
            self._body = self._environ['wsgi.input'].read(clength)
            if isinstance(self._body, bytes):
                self._body = self._body.decode('utf8')

        return self._body

    @property
    def fieldstorage(self):
        if self._fieldstorage is None:
            if self._body is not None:
                raise ReadBodyTwiceError()

            self._fieldstorage = cgi.FieldStorage(
                environ=self._environ,
                fp=self._environ['wsgi.input']
            )

        return self._fieldstorage

    @property
    def params(self):
        if self._params is None:
            self._params = VDict()

            data = compat.parse_qs(self.query)
            for k, v in data.items():
                self._params[k] = v[0]

        return self._params

    @property
    def pathparams(self):
        if self._pathparams is None:
            self._pathparams = VDict()

        return self._pathparams

    @property
    def cookie(self):
        if self._cookie is None:
            self._cookie = VDict()

            data = compat.parse_qs(self.http_header('cookie') or '')
            for k, v in data.items():
                self._cookie[k.strip()] = v[0]

        return self._cookie

    @property
    def data(self):
        if self._data is None:
            self._data = VDict()

            if isinstance(self.fieldstorage.value, list):
                for k in self.fieldstorage.keys():
                    if self.fieldstorage[k].filename:
                        self._data[k] = self.fieldstorage[k].file

                    else:
                        self._data[k] = self.fieldstorage.getfirst(k)

        return self._data

    @property
    def json(self):
        if self._json is None:
            self._json = json.loads(self.body)

        return self._json


class VDict(dict):
    _REQUIRED = object()

    @classmethod
    def validator(cls, f):
        def _(vd, key, default=cls._REQUIRED):
            return vd.take(key, f, default)
        setattr(cls, f.__name__, _)

    def take(self, key, f=None, default=_REQUIRED):
        v = self.get(key, None)
        if v is None:
            if default is self._REQUIRED:
                raise InsufficientError(key)

            else:
                return default

        else:
            if f is None:
                return v

            else:
                try:
                    return f(v)

                except Exception as e:
                    raise ValidationError(key, e)

    def regex(self, key, expr, default=_REQUIRED):
        s = self.take(key, None, default)
        if re.match(expr, s):
            return s

        raise ValidationError(key, 'invalid text')

    def email_addr(self, key, default=_REQUIRED):
        return self.regex(key, r'[^@|\s]+@[^@]+\.[^@|\s]+', default=default)

    def secure_password(self, key, default=_REQUIRED):
        reg = r'^(?=.{8,})(?=.*?[0-9]+)(?=.*?[a-z]+)(?=.*?[A-Z]+).+$'
        return self.regex(key, reg, default)

    def date(self, key, default=_REQUIRED):
        s = self.take(key, None, default)
        try:
            y = int(s[:4])
            m = int(s[4:6])
            d = int(s[6:])
            return datetime.date(y, m, d)

        except (TypeError, ValueError):
            raise ValidationError(key, 'invalid date format')

    def flag(self, key, default=_REQUIRED):
        i = self.int(key, default)
        if i in (0, 1):
            return i

        raise ValidationError(key, 'must be 0 or 1')

    def int(self, key, default=_REQUIRED):
        s = self.take(key, None, default)
        try:
            return int(s)

        except (TypeError, ValueError):
            raise ValidationError(key, 'must be int')

    def uint(self, key, default=_REQUIRED):
        i = self.int(key, default)
        if 0 <= i:
            return i

        raise ValidationError(key, 'must be a non-negative int')

    def pint(self, key, default=_REQUIRED):
        i = self.int(key, default)
        if 0 < i:
            return i

        raise ValidationError(key, 'must be positive int')
