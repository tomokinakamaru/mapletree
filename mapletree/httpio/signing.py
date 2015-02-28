# coding:utf-8

import base64
import hashlib
import hmac
from .exceptions import InvalidSignature


class Signing(object):
    def __init__(self, secret_key, hashing=hashlib.sha256):
        self._secret_key = secret_key
        self._hashing = hashing

    def sign(self, msg):
        signature = self._create_signature(msg)
        return self._encode(msg + '.' + signature)

    def unsign(self, b64msg):
        msg = self._decode(b64msg)
        if msg is not None:
            cmps = msg.rsplit('.', 1)
            if len(cmps) == 2:
                body, signature = cmps
                if signature == self._create_signature(body):
                    return body

        raise InvalidSignature()

    def _encode(self, msg):
        return base64.urlsafe_b64encode(msg).rstrip('=')

    def _decode(self, b64msg):
        try:
            padding_count = (4 - len(b64msg) % 4) % 4
            return base64.urlsafe_b64decode(b64msg + '=' * padding_count)

        except TypeError:
            return None

    def _create_signature(self, msg):
        return hmac.new(self._secret_key, msg, self._hashing).hexdigest()
