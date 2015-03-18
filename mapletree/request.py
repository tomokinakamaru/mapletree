# coding:utf-8

import cgi
import copy
import datetime
import json
import re
from xml.dom.minidom import parseString as xmldecode
from . import compat, validators
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
        """ Alias to `VDict.validator`.

        :param f: new validator function to add.
        :type f: callable
        """
        return VDict.validator(f)

    def environ(self, key):
        """ Accessor for wsgi `environ`. Returns `None` for nonexistent key.

        :param key: key to get.
        :type key: str
        """
        return self._environ.get(key)

    def http_header(self, name):
        """ Accessor for `HTTP_*` header values.
        Arg `name` is used as `'HTTP_' + name.upper()`.

        :param name: key name
        :type name: str
        """
        return self._environ.get('HTTP_' + name.upper())

    @property
    def method(self):
        """ Returns http method.
        """
        return self._environ.get('REQUEST_METHOD')

    @property
    def path(self):
        """ Returns requested path.
        """
        return self._environ.get('PATH_INFO') or '/'

    @property
    def query(self):
        """ Returns query string.
        """
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
        def _(vd, key, *args, **kwargs):
            default = kwargs.pop('default', cls._REQUIRED)
            return vd(key, f, args, kwargs, default)

        setattr(cls, f.__name__, _)

    def __call__(self, key, f=None, args=(), kwargs={}, default=_REQUIRED):
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
                    return f(v, *args, **kwargs)

                except Exception as e:
                    raise ValidationError(key, v, e)


for key in dir(validators):
    if not key.startswith('_'):
        f = getattr(validators, key)
        VDict.validator(f)
