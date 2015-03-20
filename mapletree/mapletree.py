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
        """ RequestTree instance, see detail at
        `mapletree.routetree.RequestTree`.
        """
        return self._request_tree

    @property
    def exc(self):
        """ ExceptionTree instance, see detail at
        `mapletree.routetree.ExceptionTree`.
        """
        return self._exception_tree

    @property
    def config(self):
        """ Config instance, see detail at `mapletree.config.Config`.
        """
        return self._config

    @property
    def thread(self):
        """ ThreadSpecifics instance, see detail at
        `mapletree.threadspecifics.Threadspecifics`.
        """
        return self._thread_specifics

    def run(self, port=5000, background=False):
        """ Runs this application with builtin server for testing.
        This is only for test usage, do not use in production stage.

        :param port: Port number
        :param background: Flag to run in background
        :type port: int
        :type background: bool
        """
        target = os.path.dirname(os.path.abspath(sys.argv[0]))
        driver = Driver(self, port, target, 1)
        if background:
            driver.run_background()

        else:
            driver.run()

    def scan(self, pkgname):
        """ Scans package recursively and import all modules in it.

        :param pkgname: Full package name to load
        :type pkgname: str
        """
        self._scan(import_module(pkgname))

    def _scan(self, pkg):
        pkg_file = pkg.__file__
        pkg_path = pkg_file.rstrip('/__init__.py').rstrip('/__init__.pyc')

        for _, mname, is_pkg in iter_modules([pkg_path]):
            m = import_module(pkg.__name__ + '.' + mname)

            if is_pkg:
                self._scan(m)
