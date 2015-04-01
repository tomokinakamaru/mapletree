# coding:utf-8

import requests
from mapletree import MapleTree, rsp


mt = MapleTree()
mt.autoloads.append('app.routes')


class Client(object):
    def __init__(self):
        self.session = requests.Session()

    def __call__(self, method, path, **kwargs):
        url = 'http://localhost:5000' + path
        return self.session.request(method, url, **kwargs)
