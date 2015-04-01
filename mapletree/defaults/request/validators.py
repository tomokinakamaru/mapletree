# coding:utf-8

import re
from datetime import datetime as stdlib_datetime


def int_range(string, minimum, maximum):
    """ Requires values to be an integer and in [`minimum`, `maximum`]

    :param string: Value to validate
    :param minimum: Minimum value to accept
    :param maximum: Maximum value to accept
    :type string: str
    :type minimum: int
    :type maximum: int
    """
    return _inrange(int(string), minimum, maximum, None, None)


def int_positive(string):
    """ Requires values to be an positive integer.

    :param string: Value to validate
    :type string: str
    """
    return int_range(string, 1, None)


def int_nonnegative(string):
    """ Requires values to be an non-negative integer.

    :param string: Value to validate
    :type string: str
    """
    return int_range(string, 0, None)


def int_negative(string):
    """ Requires values to be an negative integer.

    :param string: Value to validate
    :type string: str
    """
    return int_range(string, None, -1)


def flag(string):
    """ Requires values to be 0 or 1.

    :param string: Value to validate
    :type string: str
    """
    return int_range(string, 0, 1)


def float_range(string, minimum, maximum, inf, sup):
    """ Requires values to be a number and range in a certain range.

    :param string: Value to validate
    :param minimum: Minimum value to accept
    :param maximum: Maximum value to accept
    :param inf: Infimum value to accept
    :param sup: Supremum value to accept
    :type string: str
    :type minimum: float
    :type maximum: float
    :type inf: float
    :type sup: float
    """
    return _inrange(float(string), minimum, maximum, inf, sup)


def float_positive(string):
    """ Requires values to be an positive number.

    :param string: Value to validate
    :type string: str
    """
    return float_range(string, None, None, 0, None)


def float_nonnegative(string):
    """ Requires values to be an non-negative number.

    :param string: Value to validate
    :type string: str
    """
    return float_range(string, 0, None, None, None)


def float_negative(string):
    """ Requires values to be an negative number.

    :param string: Value to validate
    :type string: str
    """
    return float_range(string, None, None, None, 0)


def rate(string):
    """ Requires values to be an number between 0 and 1.

    :param string: Value to validate
    :type string: str
    """
    return float_range(string, 0, 1, None, None)


def latitude(string):
    """ Requires values to be an number between -90 and 90.

    :param string: Value to validate
    :type string: str
    """
    return float_range(string, -90, 90, None, None)


def longitude(string):
    """ Requires values to be an number between -180 and 180.

    :param string: Value to validate
    :type string: str
    """
    return float_range(string, -180, 180, None, None)


def length_range(string, minimum, maximum):
    """ Requires values' length to be in a certain range.

    :param string: Value to validate
    :param minimum: Minimum length to accept
    :param maximum: Maximum length to accept
    :type string: str
    :type minimum: int
    :type maximum: int
    """
    int_range(len(string), minimum, maximum)
    return string


def length_shorter(string, maximum):
    """ Requires values' length to be shorter than `maximum`

    :param string: Value to validate
    :param maximum: Maximum length to accept
    :type string: str
    :type maximum: int
    """
    return length_range(string, None, maximum)


def length_longer(string, minimum):
    """ Requires values' length to be longer than `minimum`

    :param string: Value to validate
    :param minimum: Minimum length to accept
    :type string: str
    :type minimum: int
    """
    return length_range(string, minimum, None)


def regex(string, expr):
    """ Requires values to match regular expression `expr`.

    :param string: Value to validate
    :param expr: Regular expression
    :type string: str
    :type expr: raw
    """
    if re.match(expr, string):
        return string

    raise ValueError('Invalid text')


def email_addr(string):
    """ Requires values to saisfy valid email address format.

    :param string: Value to validate
    :type string: str
    """
    return regex(string, r'[^@|\s]+@[^@]+\.[^@|\s]+')


def secure_password(string):
    """ Requires values to contain at least one uppercase letter,
    one lowercase letter, one digit and to be longer than 8.

    :param string: Value to validate
    :type string: str
    """
    expr = r'^(?=.{8,})(?=.*?[0-9]+)(?=.*?[a-z]+)(?=.*?[A-Z]+).+$'
    return regex(string, expr)


def date(string, fmt='%Y/%m/%d'):
    """ Requires values to be match date format `fmt`.

    :param string: Value to validate
    :param fmt: Date format
    :type string: str
    :param fmt: str
    """
    return datetime(string, fmt).date()


def datetime(string, fmt='%Y/%m/%d %H:%M:%S'):
    """ Requires values to be match datetime format `fmt`.

    :param string: Value to validate
    :param fmt: Datetime format
    :type string: str
    :param fmt: str
    """
    return stdlib_datetime.strptime(string, fmt)


def csv(string):
    """ Returns csv of string.

    :param string: Source string.
    :type string: str
    """
    return [e.strip() for e in string.split(',')]


def csv_int(string):
    """ Requires values to be int csv.

    :param string: Source string.
    :type string: str
    """
    return [int(e) for e in csv(string)]


def csv_float(string):
    """ Requires values to be number csv.

    :param string: Source string.
    :type string: str
    """
    return [float(e) for e in csv(string)]


def option(string, options):
    """ Requires values to be in `args`

    :param string: Value to validate
    :type string: str
    """
    if string in options:
        return string

    raise ValueError('Not in allowed options')


def int_option(string, options):
    """ Requires values (int) to be in `args`

    :param string: Value to validate
    :type string: str
    """
    i = int(string)
    if i in options:
        return i

    raise ValueError('Not in allowed options')


def _inrange(num, minimum, maximum, inf, sup):
    if _is_larger(num, minimum, inf) and _is_smaller(num, maximum, sup):
        return num

    raise ValueError('Out of range')


def _is_larger(num, minimum, inf):
    if minimum is None:
        if inf is None:
            return True

        else:
            return inf < num

    else:
        return minimum <= num


def _is_smaller(num, maximum, sup):
    if maximum is None:
        if sup is None:
            return True

        else:
            return num < sup

    else:
        return num <= maximum
