# coding:utf-8

import os
from importlib import import_module
from pkgutil import iter_modules


class Config(object):
    def __init__(self):
        self._data = {}
        self.stage = None

    def __getattr__(self, name):
        return self._data[name][self.stage]

    def __call__(self, f):
        self._data.setdefault(f.__name__, {}).update(f())
        return f
