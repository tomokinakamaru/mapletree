# coding:utf-8

import sys
major, minor, micro, releaselevel, serial = sys.version_info


if major == 2:
    import urlparse
    import types

    parse_qs = urlparse.parse_qs

    def response_body(s):
        return [s]

elif major == 3:
    import urllib
    import types

    parse_qs = urllib.parse.parse_qs

    def response_body(s):
        return [bytes(s, 'utf8')]
