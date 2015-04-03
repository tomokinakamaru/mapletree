# coding:utf-8

import time
from .signing import Signing


class TempToken(object):
    _LIMIT_KEY = '__expire__'

    def __init__(self, key, life_secs=60*60*24):
        self._signing = Signing(key)
        self._life_secs = life_secs

    def encode(self, **kwargs):
        kwargs[self._LIMIT_KEY] = self._expire_unixtime()
        return self._signing.sign(kwargs)

    def decode(self, token):
        data = self._signing.unsign(token)
        expire = data.pop(self._LIMIT_KEY, 0)
        if expire is None or time.time() < expire:
            return data

        raise ExpiredToken()

    def _expire_unixtime(self):
        if self._life_secs is None:
            return None

        else:
            return int(time.time()) + self._life_secs


class TempTokenException(Exception):
    pass


class ExpiredToken(TempTokenException):
    pass
