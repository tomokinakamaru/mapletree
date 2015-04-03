# coding:utf-8

import inspect
import os
import sys
from importlib import import_module
from pkgutil import iter_modules
from threading import Thread
from .driver import Driver
from .defaults.request.request import Request
from .defaults.routings.requestrouting import RequestRouting
from .defaults.routings.exceptionrouting import ExceptionRouting


class MapleTree(object):
    def __init__(self,
                 request=Request,
                 request_routing=RequestRouting(),
                 exception_routing=ExceptionRouting()):
        self._request_routing = request_routing
        self._exception_routing = exception_routing
        self._autoloads = []

    def __call__(self, environ, start_response):
        try:
            f, extra = self._request_routing(environ)
            request = Request(environ, extra)
            response = f(request)
            return response(start_response)

        except Exception as e:
            f = self._exception_routing(e)
            response = f(e)
            return response(start_response)

    @property
    def autoloads(self):
        return self._autoloads

    @property
    def req(self):
        return self._request_routing

    @property
    def exc(self):
        return self._exception_routing

    def build(self):
        caller_name = inspect.getmodule(inspect.stack()[1][0]).__name__
        if caller_name == '__main__' and not Driver.is_stub_proc():
            return

        for pkgname in self.autoloads:
            self.scan(pkgname)

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
