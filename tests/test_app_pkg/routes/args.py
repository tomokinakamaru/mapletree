# coding:utf-8

from mapletree import rsp
from test_app_pkg.shared import mt


@mt.req.get('/params')
def _(req):
    return rsp().json(**req.params)


@mt.req.post('/data')
def _(req):
    return rsp().json(**req.data)


@mt.req.post('/files')
def _(req):
    print(req.data['f'])
    return rsp().json()


@mt.req.post('/setcookie')
def _(req):
    return rsp().cookie('a', 1, secure=False)


@mt.req.get('/usecookie')
def _(req):
    return rsp().json(**req.cookie)


@mt.req.get('/clearcookie')
def _(req):
    return rsp().clear_cookie('a')


@mt.req.post('/httpscookie')
def _(req):
    return rsp().cookie('v', 2, secure=True)


@mt.req.post('/domaincookie')
def _(req):
    return rsp().cookie('v', 3, domain='.domain.com', path='/')


@mt.req.post('/json')
def _(req):
    return rsp().json(**req.json)


@mt.req.post('/readbody1')
def _(req):
    req.body
    req.fieldstorage
    return rsp().json()


@mt.req.post('/readbody2')
def _(req):
    req.fieldstorage
    req.body
    return rsp().json()
