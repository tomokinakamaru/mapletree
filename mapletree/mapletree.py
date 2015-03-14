# coding:utf-8

import os
import sys
from importlib import import_module
from pkgutil import iter_modules
from .request import Request
from .response import Response
from .config import Config
from .driver import Driver
from .exceptions import NoExceptionHandler, NotFound, MethodNotAllowed
from .routetree import RequestTree, ExceptionTree
from .threadspecifics import ThreadSpecifics


class MapleTree(object):
    def __init__(self):
        self._request_tree = RequestTree()
        self._exception_tree = ExceptionTree()
        self._config = Config()
        self._thread_specifics = ThreadSpecifics()

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)

            sys.stdout = request.environ('wsgi.errors')
            sys.stderr = request.environ('wsgi.errors')

            item, pathinfo = self._request_tree.match(request.path)

            if item is None:
                raise NotFound(request.method, request.path)

            if request.method.lower() not in item:
                raise MethodNotAllowed(request.method, request.path)

            request.pathparams.update(pathinfo)
            response = item[request.method.lower()](request)

            return response(start_response)

        except Response as response:
            return response(start_response)

        except Exception as exception:
            handler = self._exception_tree.match(exception.__class__)
            if handler is None:
                raise NoExceptionHandler(exception.__class__)

            response = handler(exception)
            return response(start_response)

    @property
    def req(self):
        return self._request_tree

    @property
    def exc(self):
        return self._exception_tree

    @property
    def config(self):
        return self._config

    @property
    def thread(self):
        return self._thread_specifics

    def run(self, port=5000, background=False):
        target = os.path.dirname(os.path.abspath(sys.argv[0]))
        driver = Driver(self, port, target, 1)
        if background:
            driver.run_background()

        else:
            driver.run()

    def scan(self, pkg_name):
        self._scan(import_module(pkg_name))

    def _scan(self, pkg):
        pkg_file = pkg.__file__
        pkg_path = pkg_file.rstrip('/__init__.py').rstrip('/__init__.pyc')

        for _, mname, is_pkg in iter_modules([pkg_path]):
            m = import_module(pkg.__name__ + '.' + mname)

            if is_pkg:
                self._scan(m)
