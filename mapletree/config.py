# coding:utf-8

import os
from importlib import import_module
from pkgutil import iter_modules


class Config(object):
    def __init__(self):
        self._data = {}
        self.stage = None

    def __getattr__(self, name):
        return getattr(self._data[self.stage], name)

    def load_package(self, pkgname):
        pkg = import_module(pkgname)
        pkg_path = os.path.dirname(pkg.__file__)

        for _, mname, is_pkg in iter_modules([pkg_path]):
            full_mname = pkg.__name__ + '.' + mname
            self.load_module(mname, full_mname)

    def load_module(self, stage, mname):
        self._data[stage] = import_module(mname)
