# coding:utf-8

import json
from datetime import date, datetime
from time import mktime
from wsgiref.handlers import format_date_time
from . import compat


class Response(Exception):
    def __init__(self):
        self._code = 200
        self._headers = {}
        self._body = ''

    def __call__(self, start_response):
        status = str(self._code) + ' ' + STATUS_PHRASES[self._code]

        headerlist = []
        for k, ls in self._headers.items():
            for e in ls:
                headerlist.append((k, e))

        start_response(status, headerlist)
        return [compat.non_unicode_str(self._body)]

    def error(self):
        """ Raises `self`. This is a shortcut method for exiting endpoint.
        """
        raise self

    def code(self, c):
        """ Sets status code.

        :param c: Status code
        :type c: int
        """
        self._code = c
        return self

    def header(self, k, v, replace=True):
        """ Sets header value. Replaces existing value if `replace` is True.
        Otherwise create a list of existing values and `v`

        :param k: Header key
        :param v: Header value
        :param replace: flag for setting mode.
        :type k: str
        :type v: str
        :type replace: bool
        """
        if replace:
            self._headers[k] = [v]

        else:
            self._headers.setdefault(k, []).append(v)

        return self

    def body(self, b):
        """ Sets response body.

        :param b: Body string
        :type b: str
        """
        self._body = b
        return self

    def ctype(self, t):
        """ Sets header value for `Content-Type`.

        :param t: Content type
        :type t: str
        """
        return self.header('Content-Type', t)

    def location(self, l):
        """ Sets header value for `Location` and sets status code 301.

        :param l: Location
        :type l: str
        """
        return self.code(301).header('Location', l)

    def cookie(self, k, v, expires=None, domain=None, path='/', secure=False):
        """ Sets cookie value.

        :param k: Name for cookie value
        :param v: Cookie value
        :param expires: Cookie expiration date
        :param domain: Cookie domain
        :param path: Cookie path
        :param secure: Flag for `https only`
        :type k: str
        :type v: str
        :type expires: datetime.datetime
        :type domain: str
        :type path: str
        :type secure: bool
        """
        ls = ['{}={}'.format(k, v)]

        if expires is not None:
            dt = format_date_time(mktime(expires.timetuple()))
            ls.append('expires={}'.format(dt))

        if domain is not None:
            ls.append('domain={}'.format(domain))

        if path is not None:
            ls.append('path={}'.format(path))

        if secure:
            ls.append('secure')

        return self.header('Set-Cookie', '; '.join(ls), False)

    def clear_cookie(self, k):
        """ Sets value to clear clients cookie.

        :param k: Cookie name to clear
        :type k: str
        """
        return self.cookie(k, '', datetime.fromtimestamp(0))

    def html(self, b):
        """ Sets content type `text/html` and body to `b`'.

        :param b: HTML string
        :type b: str
        """
        return self.ctype('text/html').body(b)

    def json(self, **kwargs):
        """ Sets content type `application/json` and
        fills body with json encoded string.

        :param kwargs: Values for body
        :type kwargs: mapping
        """
        return self.ctype('application/json').body(self._jsonencode(kwargs))

    def _jsonencode(self, obj):
        return json.dumps(obj,
                          separators=(',', ':'),
                          default=self._jsondefault)

    def _jsondefault(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y/%m/%d %H:%M:%S')

        if isinstance(obj, date):
            return obj.strftime('%Y/%m/%d')

        if isinstance(obj, (bytes, bytearray)):
            return obj.decode('utf8')

        if isinstance(obj, set):
            return [e for e in obj]

        raise TypeError('{} is not JSON serializable'.format(obj))


STATUS_PHRASES = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Moved Temporarily",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Time-out",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Large",
    415: "Unsupported Media Type",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version not supported"
}
