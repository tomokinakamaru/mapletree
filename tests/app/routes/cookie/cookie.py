# coding:utf-8

import datetime
from app.app import mt
from mapletree import rsp


@mt.req.get('/set_cookie')
def _(req):
    return rsp().cookie('cookie', 100)


@mt.req.get('/use_cookie')
def _(req):
    return rsp().json(cookie=req.cookie)


@mt.req.get('/clear_cookie')
def _(req):
    return rsp().clear_cookie('cookie')
