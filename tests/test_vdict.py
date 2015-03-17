# coding:utf-8

import pytest
from mapletree.request import VDict
from mapletree.exceptions import ValidationError, InsufficientError


def test_validator():
    @VDict.validator
    def custom(v):
        return v + '_'

    d = VDict({'a': 'test'})
    assert d.custom('a') == 'test_'


def test_take():
    d = VDict({'x': 'abc',
               'y': '100'})

    pytest.raises(InsufficientError, d, 'z')
    assert d('z', default=1) == 1
    assert d('x') == 'abc'
    assert d('y', int) == 100
    pytest.raises(ValidationError, d, 'x', int)


@pytest.mark.parametrize('email, valid',
                         [('abc@abc.com', True),
                          ('123@xyz.com', True),
                          ('12345', False),
                          ('abc@def', False)])
def test_email_addr(email, valid):
    d = VDict({'email': email})
    if valid:
        assert d.email_addr('email') == email

    else:
        pytest.raises(ValidationError, d.email_addr, 'email')


@pytest.mark.parametrize('password, valid',
                         [('password', False),
                          ('password__', False),
                          ('Password__', False),
                          ('password123', False),
                          ('Password123', True)])
def test_password(password, valid):
    d = VDict({'password': password})
    if valid:
        assert d.secure_password('password') == password

    else:
        pytest.raises(ValidationError, d.secure_password, 'password')


@pytest.mark.parametrize('date, valid',
                         [('20000101', True),
                          ('12345678', False)])
def test_date(date, valid):
    d = VDict({'date': date})
    if valid:
        d.date('date', '%Y%m%d')

    else:
        pytest.raises(ValidationError, d.date, 'date', '%Y%m%d')


def test_int():
    d = VDict({'a': '0',
               'b': '1',
               'c': '100',
               'd': '-1',
               'e': 'abc'})

    assert d('a', int) == 0
    assert d('b', int) == 1
    assert d('c', int) == 100
    assert d('d', int) == -1
    pytest.raises(ValidationError, d, 'e', int)

    assert d.flag('a') == 0
    assert d.flag('b') == 1
    pytest.raises(ValidationError, d.flag, 'c')

    assert d.int_nonnegative('a') == 0
    pytest.raises(ValidationError, d.int_nonnegative, 'd')

    assert d.int_positive('b') == 1
    pytest.raises(ValidationError, d.int_positive, 'a')

    assert d.int_negative('d') == -1
    pytest.raises(ValidationError, d.int_negative, 'a')

    assert d.int_range('a', -1, 1) == 0
    pytest.raises(ValidationError, d.int_range, 'c', -1, 1)


def test_float():
    d = VDict({'a': '1.23',
               'b': '-4.56',
               'c': '0.0',
               'd': 'abc',
               'lat': '-23.45678',
               'lon': '134.5678'})

    assert d('a', float) == 1.23
    assert d('b', float) == -4.56
    assert d('c', float) == 0
    pytest.raises(ValidationError, d, 'd', float)

    assert d.float_positive('a') == 1.23
    pytest.raises(ValidationError, d.float_positive, 'c')

    assert d.float_nonnegative('c') == 0
    pytest.raises(ValidationError, d.float_nonnegative, 'b')

    assert d.float_negative('b') == -4.56
    pytest.raises(ValidationError, d.float_negative, 'c')

    assert d.rate('c') == 0
    pytest.raises(ValidationError, d.rate, 'b')

    assert d.latitude('lat') == -23.45678
    assert d.longitude('lon') == 134.5678
    pytest.raises(ValidationError, d.latitude, 'lon')


def test_length():
    d = VDict({'a': 'this is a text',
               'b': 'this is a loger text than a'})

    assert d.length_shorter('a', 15) == d['a']
    pytest.raises(ValidationError, d.length_shorter, 'b', 15)

    assert d.length_longer('b', 15) == d['b']
    pytest.raises(ValidationError, d.length_longer, 'a', 15)


def test_csv():
    d = VDict({'a': '1,2,3,4,5',
               'b': '1.2,  3.45, 6',
               'c': 'a, b, c, d'})

    assert d.csv_int('a') == [1, 2, 3, 4, 5]
    assert d.csv_float('b') == [1.2, 3.45, 6]
    assert d.csv('c') == ['a', 'b', 'c', 'd']


def test_option():
    d = VDict({'a': 'x',
               'b': '10'})

    assert d.option('a', 'a', 'b', 'x')
    pytest.raises(ValidationError, d.option, 'a')
    assert d.int_option('b', 1, 10)
    pytest.raises(ValidationError, d.int_option, 'b', 1, 2, 3, 4)
