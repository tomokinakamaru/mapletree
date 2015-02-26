# coding:utf-8

import threading


class ThreadSpecificStorage(object):
    def __init__(self):
        self._threadlocal = threading.local()
        self._funcs = {}

    def __getattr__(self, name):
        if hasattr(self._threadlocal, name):
            return getattr(self._threadlocal, name)

        else:
            obj = self._funcs[name]()
            setattr(self._threadlocal, name, obj)
            return obj

    def __call__(self, f):
        self._funcs[f.__name__] = f
        return f
