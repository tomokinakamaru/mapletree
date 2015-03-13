# coding:utf-8


class ValidationError(Exception):
    pass


class InsufficientError(Exception):
    pass


class ReadBodyTwiceError(Exception):
    pass


class InvalidSignedMessage(Exception):
    pass


class NoExceptionHandler(Exception):
    pass


class NotFound(Exception):
    pass


class MethodNotAllowed(Exception):
    pass
