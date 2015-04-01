# coding:utf-8


class ArgContainer(dict):
    _REQUIRED = object()

    def __call__(self, key, f=None, args=(), kwargs={}, default=_REQUIRED):
        """ Retrieves a value for key with validating and default value.

        :param key: Key to retrieve.
        :param f: Validator function.
        :param args: Validator arguments.
        :param kwargs: Validator keyword arguments.
        :param default: Default value, `_REQUIRED` object if not specified.
        :type key: str
        :type f: callable
        :type args: iterable
        :type kwargs: mapping
        :type default: object
        """
        v = self.get(key, None)
        if v is None:
            if default is self._REQUIRED:
                raise InsufficientError(key)

            else:
                return default

        else:
            if f is None:
                return v

            else:
                try:
                    return f(v, *args, **kwargs)

                except Exception as e:
                    raise ValidationError(key, v, e)


class ArgContainerException(Exception):
    pass


class ValidationError(ArgContainerException):
    """ Raised when exception occurs in validation functions.
    """
    pass


class InsufficientError(ArgContainerException):
    """ Raised when a request parameter is not provided.
    """
    pass
