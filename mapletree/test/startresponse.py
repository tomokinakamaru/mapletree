# coding:utf-8


class StartResponse(object):
    def __init__(self):
        self._status = None
        self._headers = None

    def __call__(self, status, headers):
        self._status = status
        self._headers = headers

    @property
    def status(self):
        return self._status

    @property
    def headers(self):
        return self._headers
