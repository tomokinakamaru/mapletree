# coding:utf-8

import threading


class ThreadLocal(object):
    def __init__(self):
        self._threadlocal = threading.local()
        self._funcs = {}

    def __call__(self, f):
        """ Register creator functions for values.
        The name of function will be used as the name of values.

        :param f: Creator function
        :type f: callable
        """
        self._funcs[f.__name__] = f
        return f

    def __getattr__(self, name):
        """ Returns thread local value for `name`.

        :param name: Name of the value
        :type name: str
        """
        if hasattr(self._threadlocal, name):
            return getattr(self._threadlocal, name)

        else:
            try:
                f = self._funcs[name]

            except KeyError as e:
                raise UndefinedValueName(e.args[0])

            else:
                obj = f()
                setattr(self._threadlocal, name, obj)
                return obj


class ThreadLocalException(Exception):
    """ Base exception for `ThreadLocal`.
    """
    pass


class UndefinedValueName(ThreadLocalException):
    """ Exception for undefined value names.
    """
    pass
