# coding:utf-8

""" Exceptions used in MapleTree.
"""


class ValidationError(Exception):
    """ Raised when exception occurs in validation functions.
    """
    pass


class InsufficientError(Exception):
    """ Raised when a request parameter is not provided.
    """
    pass


class ReadBodyTwiceError(Exception):
    """ Raised when `wsgi.input` are read more than once.
    """
    pass


class InvalidSignedMessage(Exception):
    """ Raised when mapletree.Signing failed to decode a token.
    """
    pass


class NoExceptionHandler(Exception):
    """ Raised when no exception handlers defined.
    """
    pass


class NotFound(Exception):
    """ Raised when no endpoints defined for requested path.
    """
    pass


class MethodNotAllowed(Exception):
    """ Raised when endpoints are defined for requested path,
    but not for the requested method.
    """
    pass
