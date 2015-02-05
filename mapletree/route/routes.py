# coding:utf-8

from .base import BaseRoute, WildcardLabel


class ExceptionRoute(BaseRoute):
    def __init__(self):
        super(ExceptionRoute, self).__init__()

    def get(self, exc_cls):
        return super(ExceptionRoute, self).get(exc_cls, False)[0]

    def create_path(self, exc_cls):
        if exc_cls is BaseException:
            return []

        else:
            super_cls = exc_cls.__bases__[0]
            ls = self.create_path(super_cls)
            ls.append(exc_cls)
            return ls


class RequestRoute(BaseRoute):
    def __init__(self):
        super(RequestRoute, self).__init__()

    def create_path(self, pathstr):
        return map(self.parse_wildcard, pathstr.split('/')[1:])

    def parse_wildcard(self, elem):
        return WildcardLabel(elem[1:]) if elem.startswith(':') else elem
