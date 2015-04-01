# coding:utf-8


class StageLocal(object):
    def __init__(self):
        self._data = {}
        self.stage = None

    def __call__(self, f):
        """ Register creator functions for values.
        The name of function will be used as the name of values.

        :param f: Creator function
        :type f: callable
        """
        self._data.setdefault(f.__name__, {}).update(f())
        return f

    def __getattr__(self, name):
        """ Returns stage local value for `name`.

        :param name: Name of the value
        :type name: str
        """
        try:
            d = self._data[name]

        except KeyError as e:
            raise UndefinedValueName(e.args[0])

        else:
            try:
                return d[self.stage]

            except KeyError as e:
                raise UndefinedStageName(e.args[0])


class StageLocalException(Exception):
    """ Base exception for `StageLocal`.
    """
    pass


class UndefinedValueName(StageLocalException):
    """ Exception for undefined value names.
    """
    pass


class UndefinedStageName(StageLocalException):
    """ Exception for undefined stage names.
    """
    pass
