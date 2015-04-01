# coding:utf-8

import cgi
import json
import sys
from mapletree import compat
from .argcontainer import ArgContainer


class Request(object):
    arg_container = ArgContainer

    def __init__(self, environ, extra):
        sys.stdout = environ.get('wsgi.errors')
        sys.stderr = environ.get('wsgi.errors')
        self._environ = environ
        self._extra = self.arg_container(extra)
        self._body = None
        self._fieldstorage = None
        self._params = None
        self._cookie = None
        self._data = None
        self._json = None

    def environ(self, key):
        """ Accessor for wsgi `environ`. Returns `None` for nonexistent key.

        :param key: Key to get.
        :type key: str
        """
        return self._environ.get(key)

    def http_header(self, name):
        """ Accessor for `HTTP_*` header values.
        Arg `name` is used as `'HTTP_' + name.upper()`.

        :param name: Key name
        :type name: str
        """
        return self._environ.get('HTTP_' + name.upper())

    @property
    def body(self):
        """ String from `wsgi.input`.
        """
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
        """ `cgi.FieldStorage` from `wsgi.input`.
        """
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
        """ Parsed query string.
        """
        if self._params is None:
            self._params = self.arg_container()

            data = compat.parse_qs(self.environ('QUERY_STRING') or '')
            for k, v in data.items():
                self._params[k] = v[0]

        return self._params

    @property
    def extra(self):
        """ Extra information from routing.
        """
        return self._extra

    @property
    def cookie(self):
        """ Cookie values.
        """
        if self._cookie is None:
            self._cookie = self.arg_container()

            data = compat.parse_qs(self.http_header('cookie') or '')
            for k, v in data.items():
                self._cookie[k.strip()] = v[0]

        return self._cookie

    @property
    def data(self):
        """ Values in request body.
        """
        if self._data is None:
            self._data = self.arg_container()

            if isinstance(self.fieldstorage.value, list):
                for k in self.fieldstorage.keys():
                    if self.fieldstorage[k].filename:
                        self._data[k] = self.fieldstorage[k].file

                    else:
                        self._data[k] = self.fieldstorage.getfirst(k)

        return self._data


class RequestException(Exception):
    pass


class ReadBodyTwiceError(RequestException):
    """ Raised when `wsgi.input` are read more than once.
    """
    pass
