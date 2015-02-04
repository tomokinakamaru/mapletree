# coding:utf-8

import threading


class ThreadLocals(object):
    def __init__(self):
        self._locals = threading.local()
        self._funcs = {}

    def __getattr__(self, name):
        if hasattr(self._locals, name):
            return getattr(self._locals, name)

        else:
            obj = self._funcs[name]()
            setattr(self._locals, name, obj)
            return obj

    def __call__(self, f):
        self._funcs[f.__name__] = f
        return f
