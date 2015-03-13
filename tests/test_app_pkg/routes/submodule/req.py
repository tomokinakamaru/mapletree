# coding:utf-8

from mapletree import rsp, Request
from test_app_pkg.shared import mt


@Request.validator
def customvalidator(v):
    return v
