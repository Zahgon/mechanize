#!/usr/bin/env python
# vim:fileencoding=utf-8
# Copyright: 2018, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
import sys

is_py2 = sys.version_info.major < 3

if is_py2:
    import types
    from urllib import (
            urlencode, pathname2url, quote, addinfourl, quote_plus,
            urlopen, splitattr, splithost as urllib_splithost, getproxies,
            ftpwrapper, proxy_bypass as urllib_proxy_bypass, splitpasswd,
            splitport, splittype, splituser, splitvalue,
            unquote, unwrap, url2pathname
    )
    from urllib2 import (
            HTTPError, URLError, install_opener, build_opener, ProxyHandler
    )
    from robotparser import RobotFileParser
    from urlparse import urlsplit, urljoin, urlparse, urlunparse
    from httplib import HTTPMessage, HTTPConnection, HTTPSConnection
    from cookielib import (
            DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
            FileCookieJar, LoadError, LWPCookieJar, _debug, domain_match,
            eff_request_host, escape_path, is_HDN, lwp_cookie_str, reach,
            request_path, request_port, user_domain_match, Cookie, CookieJar,
            MozillaCookieJar, request_host)
    from cStringIO import StringIO
    from future_builtins import map  # noqa

    def is_string(x):
        pass

    def iteritems(x):
        pass

    def itervalues(x):
        pass

    def is_class(obj):
        pass

    def raise_with_traceback(exc):
        pass

    def is_mapping(x):
        pass

    codepoint_to_chr = unichr
    unicode_type = unicode
    create_response_info = HTTPMessage


else:
    import re
    from urllib.error import HTTPError, URLError
    from urllib.robotparser import RobotFileParser
    from urllib.parse import (
            urlsplit, urljoin, urlparse, urlunparse, urlencode, quote_plus,
            unquote, unwrap, quote
    )
    from urllib.request import (
            pathname2url, addinfourl, install_opener, build_opener,
            ProxyHandler, urlopen as _urlopen, getproxies, ftpwrapper,
            proxy_bypass as urllib_proxy_bypass, url2pathname, Request)
    from http.client import (
            HTTPMessage, parse_headers, HTTPConnection,
            HTTPSConnection)
    from http.cookiejar import (
            DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
            FileCookieJar, LoadError, LWPCookieJar, _debug, domain_match,
            eff_request_host, escape_path, is_HDN, lwp_cookie_str, reach,
            request_path, request_port, user_domain_match, Cookie, CookieJar,
            MozillaCookieJar, request_host)
    from io import StringIO

    def splitattr(url):
        pass

    def is_string(x):
        pass

    def iteritems(x):
        pass

    def itervalues(x):
        pass

    def is_class(obj):
        pass

    def raise_with_traceback(exc):
        pass

    codepoint_to_chr = chr
    unicode_type = str
    map = map

    # Legacy code expects HTTPMessage.getheaders()
    def getheaders(self, name):
        pass
    HTTPMessage.getheaders = getheaders

    # We want __getitem__ to return the last header not the first
    def getitem(self, name):
        pass
    HTTPMessage.__getitem__ = getitem

    # Legacy method names
    HTTPMessage.gettype = HTTPMessage.get_content_type
    HTTPMessage.getmainttype = HTTPMessage.get_content_maintype
    HTTPMessage.getsubtype = HTTPMessage.get_content_subtype

    def is_mapping(x):
        pass

    def create_response_info(fp):
        pass

    def urlopen(*a, **kw):
        pass

    _hostprog = None

    def urllib_splithost(url):
        """splithost('//host[:port]/path') --> 'host[:port]', '/path'."""
        pass

    _typeprog = None

    def splittype(url):
        """splittype('type:opaquestring') --> 'type', 'opaquestring'."""
        pass

    def splituser(host):
        """splituser('user[:passwd]@host[:port]') --> 'user[:passwd]', 'host[:port]'."""
        pass

    def splitpasswd(user):
        """splitpasswd('user:passwd') -> 'user', 'passwd'."""
        pass

    _portprog = None

    def splitport(host):
        """splitport('host:port') --> 'host', 'port'."""
        pass

    def splitvalue(attr):
        """splitvalue('attr=value') --> 'attr', 'value'."""
        pass


def as_unicode(x, encoding='utf-8', errors='strict'):
    pass


if False:
    (HTTPError, urlsplit, urljoin, urlparse, urlunparse, urlencode,
     HTTPMessage, splitattr, urllib_splithost, getproxies, ftpwrapper,
     urllib_proxy_bypass, splituser, splitpasswd, splitport,
     splitvalue, splittype, unquote, unwrap, url2pathname)
    pathname2url, RobotFileParser, URLError, quote, HTTPConnection
    HTTPSConnection, StringIO, addinfourl, install_opener, build_opener
    ProxyHandler, quote_plus, urlopen
    (DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
     FileCookieJar, LoadError, LWPCookieJar, _debug,
     domain_match, eff_request_host, escape_path, is_HDN,
     lwp_cookie_str, reach, request_path, request_port,
     user_domain_match, Cookie, CookieJar, MozillaCookieJar, request_host)
