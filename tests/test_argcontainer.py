# coding:utf-8

import pytest
from mapletree.defaults.request import validators
from mapletree.defaults.request.argcontainer import (ArgContainer,
                                                     ValidationError,
                                                     InsufficientError)


def test_basics():
    ac = ArgContainer()
    ac['a'] = '1'

    assert ac('a') == '1'
    assert ac('a', validators.int_positive) == 1


def test_invalid():
    ac = ArgContainer()
    ac['a'] = '0'

    pytest.raises(ValidationError, ac, 'a', validators.int_positive)


def test_insufficient():
    ac = ArgContainer()
    pytest.raises(InsufficientError, ac, 'a')
    assert ac('a', default=1) == 1
