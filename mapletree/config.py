# coding:utf-8

""" Utility module for automatic values switching depending on the stage.
"""

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
        """ Loads the attributes as config values in the target package.
        This imports only the first level children of package.
        Each module name is used as the stage name for it.

        :param pkgname: full package name to load
        :type pkgname: str
        """
        pkg = import_module(pkgname)
        pkg_path = os.path.dirname(pkg.__file__)

        for _, mname, is_pkg in iter_modules([pkg_path]):
            full_mname = pkg.__name__ + '.' + mname
            self.load_module(mname, full_mname)

    def load_module(self, stage, mname):
        """ Loads the attributes as config values in the target module
        with specifying the stage name for them.

        :param stage: the stage name for the config values
        :param mname: full module name to load
        :type stage: str
        :type mname: str
        """
        self._data[stage] = import_module(mname)
