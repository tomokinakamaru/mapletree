# coding:utf-8


class ValidationError(Exception):
    pass


class InsufficientError(ValidationError):
    pass


class InvalidSignature(Exception):
    pass
