# coding:utf-8

import threading


class ThreadSpecifics(object):
    def __init__(self):
        self._threadlocal = threading.local()
        self._funcs = {}

    def __getattr__(self, name):
        """ Returns thread local value for `name`.

        :param name: Name of the value
        :type name: str
        """
        if hasattr(self._threadlocal, name):
            return getattr(self._threadlocal, name)

        else:
            obj = self._funcs[name]()
            setattr(self._threadlocal, name, obj)
            return obj

    def __call__(self, f):
        """ Register function as creator of thread local value.

        :param f: Creator function
        :type f: callable
        """
        self._funcs[f.__name__] = f
        return f
