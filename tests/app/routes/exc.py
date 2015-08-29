# coding:utf-8

from app.app import mt
from mapletree import rsp
from mapletree.requesthandler import NotFound


@mt.exc.add(Exception)
def _(e):
    import traceback
    traceback.print_exc()
    return rsp().code(500)


@mt.exc.add(NotFound)
def _(e):
    return rsp().code(404)
