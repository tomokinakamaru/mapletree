# coding:utf-8

import pytest
from mapletree.helpers.stagelocal import (StageLocal,
                                          UndefinedStageName,
                                          UndefinedValueName)


def test_stagelocal():
    sl = StageLocal()

    @sl
    def value():
        return {'development': 100,
                'production': 200}

    pytest.raises(UndefinedStageName, lambda: sl.value)

    sl.stage = 'development'
    assert sl.value == 100

    sl.stage = 'production'
    assert sl.value == 200

    pytest.raises(UndefinedValueName, lambda: sl.val)
