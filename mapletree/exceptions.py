# coding:utf-8

from .httpio import ValidationError, InsufficientError, InvalidSignature


class NotFound(Exception):
    pass


class MethodNotAllowed(Exception):
    pass
