# coding:utf-8

import time
import pytest
from mapletree.helpers.temptoken import (TempToken,
                                         ExpiredToken)


def test_basics():
    tt = TempToken('token_key', None)
    data = {'a': 1}
    assert tt.decode(tt.encode(**data)) == data


def test_expire():
    tt = TempToken('token_key', 1)
    data = {'key': 'value'}

    assert tt.decode(tt.encode(**data)) == data

    token = tt.encode(**data)
    time.sleep(2)
    pytest.raises(ExpiredToken, tt.decode, token)
