# coding:utf-8

from importlib import import_module
from pkgutil import iter_modules


class Config(object):
    def __init__(self):
        self._data = {}
        self.stage = None

    def __getitem__(self, name):
        return self._data[self.stage][name]

    def load_module(self, stage, mname):
        m = import_module(mname)
        for k in dir(m):
            if not k.startswith('_'):
                self._data.setdefault(stage, {})[k] = getattr(m, k)

    def load_pkg(self, pkgname):
        pkg = import_module(pkgname)
        pkg_file = pkg.__file__
        pkg_path = pkg_file.rstrip('/__init__.py').rstrip('/__init__.pyc')

        for _, mname, is_pkg in iter_modules([pkg_path]):
            full_mname = pkg.__name__ + '.' + mname
            self.load_module(mname, full_mname)
