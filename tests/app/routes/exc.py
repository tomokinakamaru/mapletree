# coding:utf-8

from app.app import mt
from mapletree import rsp
from mapletree.defaults.routings import NotFound


@mt.exc.route(Exception)
def _(e):
    return rsp().code(500)


@mt.exc.route(NotFound)
def _(e):
    return rsp().code(404)
