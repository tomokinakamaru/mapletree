# coding:utf-8

import pytest
import threading
import time
from mapletree.helpers.threadlocal import (ThreadLocal,
                                           UndefinedValueName)


tl = ThreadLocal()


@tl
def tlocal():
    return threading.current_thread()


def test_thread_specifics():
    global subthread_success
    subthread_success = True

    def f():
        global subthread_success
        try:
            assert tl.tlocal == threading.current_thread()
            assert tl.tlocal == threading.current_thread()
            pytest.raises(UndefinedValueName, lambda: tl.value)

        except:
            subthread_success = False

        else:
            subthread_success = True

    t = threading.Thread(target=f)
    t.start()
    t.join()
    assert subthread_success
