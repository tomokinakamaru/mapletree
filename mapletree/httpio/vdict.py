# coding:utf-8

from .exceptions import ValidationError, InsufficientError


class VDict(dict):
    REQUIRED = object()

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
