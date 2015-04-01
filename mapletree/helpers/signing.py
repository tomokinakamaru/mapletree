# coding:utf-8

import base64
import hashlib
import hmac
import json
from mapletree import compat


class Signing(object):
    def __init__(self, secret_key, hash_f=hashlib.sha256):
        """ Initialize.

        :param secret_key: Key for data signing/unsigning
        :param hash_f: Hash function
        :type secret_key: str
        :type hash_f: callable
        """
        self._secret_key = compat.non_unicode_str(secret_key)
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
            signature = self._create_signature(jsonstr)
            return self._b64encode(jsonstr + '.' + signature)

    def unsign(self, b64msg):
        """ Retrieves data from signed token.

        :param b64msg: Token to unsign
        :type b64msg: str
        """
        msg = self._b64decode(b64msg)
        try:
            body, signature = msg.rsplit('.', 1)

        except ValueError as e:
            raise MalformedSigendMessage(e.args[0])

        else:
            if signature == self._create_signature(body):
                try:
                    return json.loads(body)

                except ValueError as e:
                    raise MalformedSigendMessage(e.args[0])

            else:
                raise BadSignature()

    def _b64encode(self, msgstr):
        msg = compat.non_unicode_str(msgstr)
        return base64.urlsafe_b64encode(msg).rstrip(b'=').decode('utf8')

    def _b64decode(self, b64msgstr):
        try:
            padding = (4 - len(b64msgstr) % 4) % 4
            b64msg = compat.non_unicode_str(b64msgstr + '=' * padding)
            return base64.urlsafe_b64decode(b64msg).decode('utf8')

        except (TypeError, UnicodeDecodeError) as e:
            raise MalformedSigendMessage(e.args[0])

    def _create_signature(self, msgstr):
        b = compat.non_unicode_str(msgstr)
        return hmac.new(self._secret_key, b, self._hash_f).hexdigest()


class SigningException(Exception):
    """ Base exception for `Signing`.
    """
    pass


class DataSignError(SigningException):
    """ Exception for signing error.
    """
    pass


class DataUnsignError(SigningException):
    """ Exception for unsignin error.
    """
    pass


class MalformedSigendMessage(DataUnsignError):
    """ Exception for malformed token.
    """
    pass


class BadSignature(DataUnsignError):
    """ Exception for unmaching signature.
    """
    pass
