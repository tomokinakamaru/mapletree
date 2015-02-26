# coding:utf-8

import urllib
import urlparse
from .signing import Signing
from .vdict import VDict


_MSG_NO_SECRET_KEY = 'Session requires secret key (Session.set_secret_key)'


class Session(VDict):
    COOKIE_NAME = 'SESSION'
    _signing = None

    @classmethod
    def set_secret_key(cls, key):
        cls._signing = Signing(key)

    @classmethod
    def decode(cls, token):
        session = Session()

        if cls._signing is None:
            raise Exception(_MSG_NO_SECRET_KEY)

        msg = cls._signing.unsign(token or '')
        data = urlparse.parse_qs(msg)
        for k, v in data.items():
            session[k] = v[0]

        return session

    def encode(self):
        msg = urllib.urlencode(self)

        if self._signing is None:
            raise Exception(_MSG_NO_SECRET_KEY)

        return self._signing.sign(msg)
