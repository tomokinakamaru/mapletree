# coding:utf-8

from mapletree import rsp
from test_app_pkg.shared import mt


@mt.req.get('/html')
def _(req):
    return rsp().html('<html>{}</html>'.format(req.params('a')))


@mt.req.get('/location')
def _(req):
    return rsp().location('http://localhost:5000/')


@mt.req.get('/jsonencode')
def _(req):
    from datetime import datetime
    return rsp().json(**{
        'set': set([1, 2, 3]),
        'bytes': b'bytesbytes',
        'bytearray': bytearray(b'bytearray'),
        'datetime': datetime.utcnow()
    })


@mt.req.get('/not_json_serializable')
def _(req):
    try:
        return rsp().json(v=lambda: None)

    except TypeError:
        return rsp().code(500)
