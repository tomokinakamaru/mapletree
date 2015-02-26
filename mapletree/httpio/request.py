# coding:utf-8

import cgi
import copy
import urlparse
from json import loads as jsondecode
from xml.dom.minidom import parseString as xmldecode
from .session import Session
from .vdict import VDict


class Request(object):
    def __init__(self, environ):
        self._environ = environ
        self._fieldstorage = None
        self._params = None
        self._cookie = None
        self._data = None
        self._json = None
        self._xml = None
        self._session = None
        self._pathparams = None

    def copy_environ(self):
        return copy.deepcopy(self._environ)

    def environ(self, key):
        return self._environ.get(key)

    def http_header(self, name):
        return self._environ.get('HTTP_' + name.upper())

    @property
    def method(self):
        return self._environ['REQUEST_METHOD']

    @property
    def script_name(self):
        return self._environ['SCRIPT_NAME']

    @property
    def path(self):
        return self._environ['PATH_INFO'] or '/'

    @property
    def ctype(self):
        return self._environ['CONTENT_TYPE']

    @property
    def clength(self):
        return self._environ['CONTENT_LENGTH']

    @property
    def server_name(self):
        return self._environ['SERVER_NAME']

    @property
    def port(self):
        return self._environ['SERVER_PORT']

    @property
    def protocol(self):
        return self._environ['SERVER_PROTOCOL']

    @property
    def query(self):
        return self._environ['QUERY_STRING']

    @property
    def fieldstorage(self):
        if self._fieldstorage is None:
            self._fieldstorage = cgi.FieldStorage(
                environ=self._environ,
                fp=self._environ['wsgi.input']
            )

        return self._fieldstorage

    @property
    def params(self):
        if self._params is None:
            self._params = VDict()

            data = urlparse.parse_qs(self.query)
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

            data = urlparse.parse_qs(self.http_header('cookie') or '')
            for k, v in data.items():
                self._cookie[k.strip()] = v[0]

        return self._cookie

    @property
    def data(self):
        if self._data is None:
            self._data = VDict()

            if isinstance(self.fieldstorage.value, list):
                for k in self.fieldstorage.keys():
                    self._data[k] = self.fieldstorage.getfirst(k)

        return self._data

    @property
    def json(self):
        if self._json is None:
            if isinstance(self.fieldstorage.value, str):
                try:
                    self._json = jsondecode(self.fieldstorage.value)

                except TypeError, ValueError:
                    self._json = {}

            else:
                self._json = {}

        return self._json

    @property
    def xml(self):
        if self._xml is None:
            if isinstance(self.fieldstorage.value, str):
                try:
                    self._xml = xmldecode(self.fieldstorage.value)

                except:
                    self._xml = xmldecode('<xml></xml>')

            else:
                self._xml = xmldecode('<xml></xml>')

        return self._xml

    @property
    def session(self):
        if self._session is None:
            token = self.cookie.get(Session.COOKIE_NAME)
            self._session = Session.decode(token)

        return self._session
