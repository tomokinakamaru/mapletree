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

    pytest.raises(InsufficientError, d.take, 'z')
    assert d.take('z', None, 1) == 1
    assert d.take('x', None) == 'abc'
    assert d.take('y', int) == 100
    pytest.raises(ValidationError, d.take, 'x', int)


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
        d.date('date')

    else:
        pytest.raises(ValidationError, d.date, 'date')


def test_int():
    d = VDict({'a': '0',
               'b': '1',
               'c': '100',
               'd': '-1',
               'e': 'abc'})

    assert d.int('a') == 0
    assert d.int('b') == 1
    assert d.int('c') == 100
    assert d.int('d') == -1
    pytest.raises(ValidationError, d.int, 'e')

    assert d.flag('a') == 0
    assert d.flag('b') == 1
    pytest.raises(ValidationError, d.flag, 'c')

    assert d.uint('a') == 0
    pytest.raises(ValidationError, d.uint, 'd')

    assert d.pint('b') == 1
    pytest.raises(ValidationError, d.pint, 'a')
