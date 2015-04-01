# coding:utf-8

import sys

major, minor, micro, releaselevel, serial = sys.version_info


if major == 2:
    # parse_qs
    import urlparse
    parse_qs = urlparse.parse_qs

    # non_unicode_str
    def non_unicode_str(s):
        return s.encode('utf8') if isinstance(s, unicode) else s

elif major == 3:
    # parse_qs
    import urllib
    parse_qs = urllib.parse.parse_qs

    # non_unicode_str
    def non_unicode_str(s):
        return s.encode('utf8') if isinstance(s, str) else s
