# coding:utf-8

from dictree import Dictree


class ExceptionHandler(object):
    def __init__(self):
        self._tree = Dictree()

    @property
    def tree(self):
        return self._tree

    @staticmethod
    def parse_exc(exc_cls):
        if exc_cls is Exception:
            return ()

        else:
            super_cls = exc_cls.__bases__[0]
            return ExceptionHandler.parse_exc(super_cls) + (exc_cls,)

    def __call__(self, exc):
        key = self.parse_exc(exc.__class__)
        try:
            f, _ = self.tree.find(key)

        except KeyError:
            raise NoExceptionHandler()

        else:
            return f

    def add(self, exc_cls):
        def _(f):
            self.tree[self.parse_exc(exc_cls)] = f
            return f
        return _

    def merge(self, handler):
        self.tree.update(handler.tree)


class NoExceptionHandler(Exception):
    pass
