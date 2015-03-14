# coding:utf-8

import threading
import time
from mapletree.threadspecifics import ThreadSpecifics


ts = ThreadSpecifics()


@ts
def tlocal():
    return threading.current_thread()


def test_thread_specifics():
    global subthread_success
    subthread_success = True

    def f():
        global subthread_success
        try:
            assert ts.tlocal == threading.current_thread()
            assert ts.tlocal == threading.current_thread()

        except AssertionError:
            subthread_success = False

        else:
            subthread_success = True

    t = threading.Thread(target=f)
    t.start()
    t.join()
    assert subthread_success
