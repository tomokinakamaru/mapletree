# coding:utf-8

import base64
import hashlib
import hmac
import json
from .exceptions import InvalidSignedMessage


class Signing(object):
    def __init__(self, secret_key, hash_f=hashlib.sha256):
        self._secret_key = secret_key.encode('utf8')
        self._hash_f = hash_f

    def sign(self, data):
        jsonstr = json.dumps(data, separators=(',', ':'))
        signature = self.create_signature(jsonstr)
        return self.b64encode(jsonstr + '.' + signature)

    def unsign(self, b64msg):
        msg = self.b64decode(b64msg)
        try:
            body, signature = msg.rsplit('.', 1)

        except ValueError:
            raise InvalidSignedMessage()

        else:
            if signature == self.create_signature(body):
                try:
                    return json.loads(body)

                except ValueError:
                    raise InvalidSignedMessage()

            else:
                raise InvalidSignedMessage()

    def b64encode(self, msgstr):
        msg = msgstr.encode('utf8')
        return base64.urlsafe_b64encode(msg).rstrip(b'=').decode('utf8')

    def b64decode(self, b64msgstr):
        try:
            padding = (4 - len(b64msgstr) % 4) % 4
            b64msg = b64msgstr + '=' * padding
            b64msg = b64msg.encode('utf8')
            return base64.urlsafe_b64decode(b64msg).decode('utf8')

        except (TypeError, UnicodeDecodeError):
            import traceback
            traceback.print_exc()
            raise InvalidSignedMessage()

    def create_signature(self, msgstr):
        b = msgstr.encode('utf8')
        return hmac.new(self._secret_key, b, self._hash_f).hexdigest()
