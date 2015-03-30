# coding:utf-8

import base64
import hashlib
import hmac
import json
import sys


class Signing(object):
    def __init__(self, secret_key, hash_f=hashlib.sha256):
        """ Initialize.

        :param secret_key: Key for data signing/unsigning
        :param hash_f: Hash function
        :type secret_key: str
        :type hash_f: callable
        """
        self._secret_key = to_byte_string(secret_key)
        self._hash_f = hash_f

    def sign(self, data):
        """ Create url-safe signed token.

        :param data: Data to sign
        :type data: object
        """
        try:
            jsonstr = json.dumps(data, separators=(',', ':'))

        except TypeError as e:
            raise DataSignError(e.args[0])

        else:
            signature = self.create_signature(jsonstr)
            return self.b64encode(jsonstr + '.' + signature)

    def unsign(self, b64msg):
        """ Retrieves data from signed token.

        :param b64msg: Token to unsign
        :type b64msg: str
        """
        msg = self.b64decode(b64msg)
        try:
            body, signature = msg.rsplit('.', 1)

        except ValueError as e:
            raise MalformedSigendMessage(e.args[0])

        else:
            if signature == self.create_signature(body):
                try:
                    return json.loads(body)

                except ValueError as e:
                    raise MalformedSigendMessage(e.args[0])

            else:
                raise BadSignature()

    def b64encode(self, msgstr):
        msg = to_byte_string(msgstr)
        return base64.urlsafe_b64encode(msg).rstrip(b'=').decode('utf8')

    def b64decode(self, b64msgstr):
        try:
            padding = (4 - len(b64msgstr) % 4) % 4
            b64msg = to_byte_string(b64msgstr + '=' * padding)
            return base64.urlsafe_b64decode(b64msg).decode('utf8')

        except (TypeError, UnicodeDecodeError) as e:
            raise MalformedSigendMessage(e.args[0])

    def create_signature(self, msgstr):
        b = to_byte_string(msgstr)
        return hmac.new(self._secret_key, b, self._hash_f).hexdigest()


is_py3 = sys.version_info[0] == 3


def to_byte_string(s):
    if is_py3:
        if isinstance(s, str):
            return s.encode('utf8')

        else:
            return s

    else:
        if isinstance(s, unicode):
            return s.encode('utf8')

        else:
            return s


class SigningException(Exception):
    pass


class DataSignError(SigningException):
    pass


class DataUnsignError(SigningException):
    pass


class MalformedSigendMessage(DataUnsignError):
    pass


class BadSignature(DataUnsignError):
    pass
