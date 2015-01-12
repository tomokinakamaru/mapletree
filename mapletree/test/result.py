# coding:utf-8


class Result(object):
    def __init__(self, body, start_response):
        self._code = int(start_response.status[:3])

        self._headers = {}
        for k, v in start_response.headers:
            self._headers.setdefault(k, []).append(v)

        self._body = ''
        for b in body:
            self._body += b

    @property
    def code(self):
        return self._code

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body
