# coding:utf-8

from dictree import Dictree


class ExceptionHandler(object):
    def __init__(self):
        self._tree = Dictree()

    @property
    def tree(self):
        return self._tree

    @classmethod
    def parse_exc(cls, exc_cls):
        if exc_cls is Exception:
            return ()

        else:
            super_cls = exc_cls.__bases__[0]
            return cls.parse_exc(super_cls) + (exc_cls,)

    def __call__(self, exc):
        key = self.parse_exc(exc.__class__)

        try:
            f, _ = self.tree.find(key)

        except KeyError:
            raise NoExceptionHandler()

        return f

    def add(self, exc_cls):
        def _(f):
            key = self.parse_exc(exc_cls)
            self.tree[key] = f
            return f
        return _

    def merge(self, handler):
        for key, f in handler.tree.items():
            self.add(key[-1])(f)


class NoExceptionHandler(Exception):
    pass
