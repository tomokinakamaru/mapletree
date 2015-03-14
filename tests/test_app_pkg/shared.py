# coding:utf-8

import threading
from mapletree import MapleTree

mt = MapleTree()


@mt.thread
def threadid():
    return threading.current_thread()
