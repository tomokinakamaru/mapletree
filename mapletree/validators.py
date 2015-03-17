# coding:utf-8

import re
from datetime import datetime as stdlib_datetime


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


def int_range(string, minimum, maximum):
    return _inrange(int(string), minimum, maximum, None, None)


def int_positive(string):
    return int_range(string, 1, None)


def int_nonnegative(string):
    return int_range(string, 0, None)


def int_negative(string):
    return int_range(string, None, -1)


def flag(string):
    return int_range(string, 0, 1)


def float_range(string, minimum, maximum, inf, sup):
    return _inrange(float(string), minimum, maximum, inf, sup)


def float_positive(string):
    return float_range(string, None, None, 0, None)


def float_nonnegative(string):
    return float_range(string, 0, None, None, None)


def float_negative(string):
    return float_range(string, None, None, None, 0)


def rate(string):
    return float_range(string, 0, 1, None, None)


def latitude(string):
    return float_range(string, -90, 90, None, None)


def longitude(string):
    return float_range(string, -180, 180, None, None)


def length_range(string, minimum, maximum):
    int_range(len(string), minimum, maximum)
    return string


def length_shorter(string, maximum):
    return length_range(string, None, maximum)


def length_longer(string, minimum):
    return length_range(string, minimum, None)


def regex(string, expr):
    if re.match(expr, string):
        return string

    raise ValueError('Invalid text')


def email_addr(string):
    return regex(string, r'[^@|\s]+@[^@]+\.[^@|\s]+')


def secure_password(string):
    expr = r'^(?=.{8,})(?=.*?[0-9]+)(?=.*?[a-z]+)(?=.*?[A-Z]+).+$'
    return regex(string, expr)


def date(string, fmt='%Y/%m/%d'):
    return datetime(string, fmt).date()


def datetime(string, fmt='%Y/%m/%d %H:%M:%S'):
    return stdlib_datetime.strptime(string, fmt)


def csv(string):
    return [e.strip() for e in string.split(',')]


def csv_int(string):
    return [int(e.strip()) for e in string.split(',')]


def csv_float(string):
    return [float(e.strip()) for e in string.split(',')]


def option(string, *args):
    if string in args:
        return string

    raise ValueError('Not in allowed options')


def int_option(string, *args):
    i = int(string)
    if i in args:
        return i

    raise ValueError('Not in allowed options')
