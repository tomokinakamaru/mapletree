# coding:utf-8

import threading
from mapletree import rsp
from mapletree.exceptions import NotFound, MethodNotAllowed
from test_app_pkg.shared import mt


@mt.req.get('/')
def _(req):
    return rsp()


@mt.req.post('/')
def _(req):
    return rsp()


@mt.req.put('/')
def _(req):
    return rsp()


@mt.req.delete('/')
def _(req):
    return rsp()


@mt.req.options('/')
def _(req):
    return rsp()


@mt.req.head('/')
def _(req):
    return rsp()


@mt.req.patch('/')
def _(req):
    return rsp()


@mt.req.get('/get_only')
def _(req):
    return rsp()


@mt.req.get('/error')
def _(req):
    rsp().code(500).error()


@mt.req.get('/unhandled_error')
def _(req):
    raise ZeroDivisionError()


@mt.exc(NotFound)
def _(e):
    return rsp().code(404)


@mt.exc(MethodNotAllowed)
def _(e):
    return rsp().code(405)


@mt.req.get('/config')
def _(req):
    return rsp().json(v=mt.config.value)


@mt.req.get('/tss')
def _(req):
    return rsp().json(v=threading.current_thread() is mt.thread.threadid)
