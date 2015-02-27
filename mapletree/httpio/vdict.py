# coding:utf-8

import re
from types import MethodType
from .exceptions import ValidationError, InsufficientError


class VDict(dict):
    REQUIRED = object()
    _ext = {}

    @classmethod
    def extend(cls, f):
        _ = lambda vd, key, default=cls.REQUIRED: vd.take(key, f, default)
        setattr(cls, f.__name__, MethodType(_, None, cls))

    def take(self, key, f=None, default=REQUIRED):
        v = self.get(key, None)
        if v is None:
            if default is self.REQUIRED:
                raise InsufficientError(key)

            else:
                return default

        else:
            if f is None:
                return v

            else:
                try:
                    return f(v)

                except Exception as e:
                    raise ValidationError(key, e)

    def regex(self, key, expr, default=REQUIRED):
        return self.take(key, vldt_regex(expr), default)

    def email_addr(self, key, default=REQUIRED):
        return self.take(key, vldt_regex(r'[^@|\s]+@[^@]+\.[^@|\s]+'), default)

    def int(self, key, default=REQUIRED):
        return self.take(key, vldt_int, default)

    def flag(self, key, default=REQUIRED):
        i = self.int(key, default)
        if i in (0, 1):
            return i

        raise ValidationError('must be 0 or 1')

    def uint(self, key, default=REQUIRED):
        i = self.int(key, default)
        if 0 <= i:
            return i

        raise ValidationError('must be non-negative int')


def vldt_regex(expr):
    def _(v):
        if re.match(expr, v):
            return v

        raise Exception('{} does not match regex "{}"'.format(v, expr))

    return _


def vldt_int(v):
    try:
        return int(v)

    except ValueError:
        raise Exception('must be int')
