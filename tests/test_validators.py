# coding:utf-8

import pytest
from datetime import date
from mapletree.defaults.request import validators as V


def test_int_positive():
    assert V.int_positive('1') == 1
    pytest.raises(Exception, V.int_positive, '0')


def test_int_nonnegative():
    assert V.int_nonnegative('0') == 0
    pytest.raises(Exception, V.int_nonnegative, '-1')


def test_int_negative():
    assert V.int_negative('-1') == -1
    pytest.raises(Exception, V.int_negative, '0')


def test_flag():
    assert V.flag('0') == 0
    pytest.raises(Exception, V.flag, '100')


def test_float_positive():
    assert V.float_positive('3.14') == 3.14
    pytest.raises(Exception, V.float_positive, '0')


def test_float_nonnegative():
    assert V.float_nonnegative('0.0') == 0
    pytest.raises(Exception, V.float_nonnegative, '-3.14')


def test_float_negative():
    assert V.float_negative('-3.14') == -3.14
    pytest.raises(Exception, V.float_negative, '0')


def test_rate():
    assert V.rate('1.0') == 1
    pytest.raises(Exception, V.rate, '1.01')


def test_latitide():
    assert V.latitude('-90') == -90
    pytest.raises(Exception, V.latitude, '-180')


def test_longitude():
    assert V.longitude('180') == 180
    pytest.raises(Exception, V.longitude, '-270')


def test_length_shorter():
    assert V.length_shorter('abcde', 5) == 'abcde'
    pytest.raises(Exception, V.length_shorter, 'abcde', 4)


def test_length_longer():
    assert V.length_longer('abcde', 5) == 'abcde'
    pytest.raises(Exception, V.length_longer, 'abcde', 6)


def test_email_addr():
    assert V.email_addr('abc@def.com') == 'abc@def.com'
    pytest.raises(Exception, V.email_addr, 'abc@def')


def test_secure_password():
    assert V.secure_password('Password123') == 'Password123'
    pytest.raises(Exception, V.secure_password, 'password')


def test_date():
    assert V.date('1990/01/01') == date(1990, 1, 1)
    pytest.raises(Exception, V.date, '19900101')


def test_csv_int():
    assert V.csv_int('1, 2, 3') == [1, 2, 3]
    pytest.raises(Exception, V.csv_int, '1, a, b')


def test_csv_float():
    assert V.csv_float('1.0, 2, 3.14') == [1, 2, 3.14]
    pytest.raises(Exception, V.csv_float, '1, a, b')


def test_option():
    assert V.option('1', ['1', '2']) == '1'
    pytest.raises(Exception, V.option, '3', ['1', '2'])


def test_int_option():
    assert V.int_option('1', [1, 2]) == 1
    pytest.raises(Exception, V.int_option, '3', [1, 2])


def test_file():
    with open('README.rst') as fp:
        v = ('README.rst', fp)
        assert V.file(v, 'rst') == v
        pytest.raises(Exception, V.file, v, 'txt')
        pytest.raises(Exception, V.file, 'test', 'aaa')
