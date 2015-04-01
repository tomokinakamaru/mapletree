# coding:utf-8

from app.app import mt
from mapletree import rsp


@mt.req.get('/')
def _(req):
    return rsp()


@mt.req.get('/params')
def _(req):
    return rsp().json(**req.params)


@mt.req.post('/data')
def _(req):
    return rsp().json(**req.data)


@mt.req.post('/read_twice1')
def _(req):
    req.body
    req.data
    return rsp()


@mt.req.post('/read_twice2')
def _(req):
    req.data
    req.body
    return rsp()


@mt.req.get('/extra/:label')
def _(req):
    return rsp().json(**req.extra)
