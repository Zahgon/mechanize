"""Fork of urllib2.

When reading this, don't assume that all code in here is reachable.  Code in
the rest of mechanize may be used instead.

Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 Python
Software Foundation; All Rights Reserved

Copyright 2002-2009 John J Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file
LICENSE included with the distribution).

"""

# XXX issues:
# If an authentication error handler that tries to perform
# authentication for some reason but fails, how should the error be
# signalled?  The client needs to know the HTTP error code.  But if
# the handler knows that the problem was, e.g., that it didn't know
# that hash algo that requested in the challenge, it would be good to
# pass that information along to the client, too.
# ftp errors aren't handled cleanly
# check digest against correct (i.e. non-apache) implementation

# Possible extensions:
# complex proxies  XXX not sure what exactly was meant by this
# abstract factory for opener

from __future__ import absolute_import

import base64
import bisect
import copy
import hashlib
import logging
import os
import platform
import posixpath
import re
import socket
import sys
import time
from collections import OrderedDict
from functools import partial
from io import BufferedReader, BytesIO

from . import _rfc3986
from ._clientcookie import CookieJar
from ._headersutil import normalize_header_name
from ._response import closeable_response
from .polyglot import (HTTPConnection, HTTPError, HTTPSConnection, URLError,
                       as_unicode, create_response_info, ftpwrapper,
                       getproxies, is_class, is_mapping, is_py2, is_string,
                       iteritems, map, raise_with_traceback, splitattr,
                       splitpasswd, splitport, splittype, splituser,
                       splitvalue, unquote, unwrap, url2pathname,
                       urllib_proxy_bypass, urllib_splithost, urlparse,
                       urlsplit, urlunparse)


def sha1_digest(data):
    pass


def md5_digest(data):
    pass


if platform.python_implementation() == 'PyPy':
    def create_readline_wrapper(fh):
        pass
else:
    def create_readline_wrapper(fh):
        pass


splithost = urllib_splithost


# used in User-Agent header sent
__version__ = sys.version[:3]

_opener = None


def urlopen(url, data=None):
    pass


def install_opener(opener):
    pass


# copied from cookielib.py
_cut_port_re = re.compile(r":\d+$")


def request_host(request):
    """Return request-host, as defined by RFC 2965.

    Variation from RFC: returned value is lowercased, for convenient
    comparison.

    """
    pass


PERCENT_RE = re.compile(b"%[a-fA-F0-9]{2}")
ZONE_ID_CHARS = set(bytearray(
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZ" b"abcdefghijklmnopqrstuvwxyz" b"0123456789._!-"
))
USERINFO_CHARS = ZONE_ID_CHARS | set(bytearray(b"$&'()*+,;=:"))
PATH_CHARS = USERINFO_CHARS | set(bytearray(b'@/~'))
QUERY_CHARS = FRAGMENT_CHARS = PATH_CHARS | {ord(b"?")}


def fix_invalid_bytes_in_url_component(component, allowed_chars=PATH_CHARS):
    pass


def normalize_url(url):
    pass


class Request:

    def __init__(self, url, data=None, headers={},
                 origin_req_host=None, unverifiable=False, method=None):
        # unwrap('<URL:type://host/path>') --> 'type://host/path'
        pass

    def __getattr__(self, attr):
        # XXX this is a fallback mechanism to guard against these
        # methods getting called in a non-standard order.  this may be
        # too complicated and/or unnecessary.
        # XXX should the __r_XXX attributes be public?
        if attr[:12] == '_Request__r_':
            name = attr[12:]
            if hasattr(Request, 'get_' + name):
                getattr(self, 'get_' + name)()
                return getattr(self, attr)
        raise AttributeError(attr)

    def get_method(self):
        ' The method used for HTTP requests '
        pass

    # XXX these helper methods are lame

    def set_data(self, data):
        ' Set the data (a bytestring) to be sent with this request '
        pass
    add_data = set_data

    def has_data(self):
        ' True iff there is some data to be sent with this request '
        pass

    def get_data(self):
        ' The data to be sent with this request '
        pass

    def get_full_url(self):
        pass

    @property
    def full_url(self):
        # In python 3 this is a deleteable and settable property, which when
        # deleted gets set to None. But this interface does not seem to be used
        # by any stdlib code, so this should be sufficient.
        pass

    def get_type(self):
        pass

    def get_host(self):
        pass

    def get_selector(self):
        pass

    def set_proxy(self, host, type):
        pass

    def has_proxy(self):
        """Private method."""
        pass

    def get_origin_req_host(self):
        pass

    def is_unverifiable(self):
        pass

    def add_header(self, key, val=None):
        ''' Add the specified header, replacing existing one, if needed. If val
        is None, remove the header. '''
        pass

    def add_unredirected_header(self, key, val):
        ''' Same as :meth:`add_header()` except that this header will not
        be sent for redirected requests. '''
        pass

    def has_header(self, header_name):
        ''' Check if the specified header is present '''
        pass

    def get_header(self, header_name, default=None):
        ''' Get the value of the specified header. If absent, return `default`
        '''
        pass

    def header_items(self):
        ''' Get a copy of all headers for this request as a list of 2-tuples
        '''
        pass


class OpenerDirector(object):

    def __init__(self):
        client_version = "Python-urllib/%s" % __version__
        self.addheaders = [('User-agent', client_version)]
        self.finalize_request_headers = None
        # manage the individual handlers
        self.handlers = []
        self.handle_open = {}
        self.handle_error = {}
        self.process_response = {}
        self.process_request = {}

    def add_handler(self, handler):
        pass

    def close(self):
        # Only exists for backwards compatibility.
        pass

    def _call_chain(self, chain, kind, meth_name, *args):
        # Handlers raise an exception if no one else should try to handle
        # the request, or return None if they can't but another handler
        # could.  Otherwise, they return the response.
        pass

    def _open(self, req, data=None):
        pass

    def error(self, proto, *args):
        pass

# XXX probably also want an abstract factory that knows when it makes
# sense to skip a superclass in favor of a subclass and when it might
# make sense to include both


def build_opener(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP, FTP and when applicable, HTTPS.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """
    pass


class BaseHandler:
    handler_order = 500

    def add_parent(self, parent):
        pass

    def close(self):
        # Only exists for backwards compatibility
        pass

    def __lt__(self, other):
        return self.handler_order < getattr(
                other, 'handler_order', sys.maxsize)

    def __copy__(self):
        return self.__class__()


class HTTPErrorProcessor(BaseHandler):
    """Process HTTP error responses.

    The purpose of this handler is to to allow other response processors a
    look-in by removing the call to parent.error() from
    AbstractHTTPHandler.

    For non-2xx error codes, this just passes the job on to the
    Handler.<proto>_error_<code> methods, via the OpenerDirector.error method.
    Eventually, HTTPDefaultErrorHandler will raise an HTTPError if no other
    handler handles the error.

    """
    handler_order = 1000  # after all other processors

    def http_response(self, request, response):
        pass

    https_response = http_response


class HTTPDefaultErrorHandler(BaseHandler):

    def http_error_default(self, req, fp, code, msg, hdrs):
        # why these error methods took the code, msg, headers args in the first
        # place rather than a response object, I don't know, but to avoid
        # multiple wrapping, we're discarding them

        pass


class HTTPRedirectHandler(BaseHandler):
    # maximum number of redirections to any single URL
    # this is needed because of the state that cookies introduce
    max_repeats = 4
    # maximum total number of redirections (regardless of URL) before
    # assuming we're in a loop
    max_redirections = 10

    # Implementation notes:

    # To avoid the server sending us into an infinite loop, the request
    # object needs to track what URLs we have already seen.  Do this by
    # adding a handler-specific attribute to the Request object.  The value
    # of the dict is used to count the number of times the same URL has
    # been visited.  This is needed because visiting the same URL twice
    # does not necessarily imply a loop, thanks to state introduced by
    # cookies.

    # Always unhandled redirection codes:
    # 300 Multiple Choices: should not handle this here.
    # 304 Not Modified: no need to handle here: only of interest to caches
    #     that do conditional GETs
    # 305 Use Proxy: probably not worth dealing with here
    # 306 Unused: what was this for in the previous versions of protocol??

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return a Request or None in response to a redirect.

        This is called by the http_error_30x methods when a
        redirection response is received.  If a redirection should
        take place, return a new Request to allow http_error_30x to
        perform the redirect.  Otherwise, raise HTTPError if no-one
        else should try to handle this url.  Return None if you can't
        but another Handler might.
        """
        pass

    def http_error_302(self, req, fp, code, msg, headers):
        # Some servers (incorrectly) return multiple Location headers
        # (so probably same goes for URI).  Use first header.
        pass

    http_error_301 = http_error_303 = http_error_307 = http_error_302
    http_error_refresh = http_error_308 = http_error_302

    inf_msg = "The HTTP server returned a redirect error that would " \
              "lead to an infinite loop.\n" \
              "The last 30x error message was:\n"


def _parse_proxy(proxy):
    """Return (scheme, user, password, host/port) given a URL or an authority.

    If a URL is supplied, it must have an authority (host:port) component.
    According to RFC 3986, having an authority component means the URL must
    have two slashes after the scheme:

    >>> _parse_proxy('file:/ftp.example.com/')
    Traceback (most recent call last):
    ValueError: proxy URL with no authority: 'file:/ftp.example.com/'

    The first three items of the returned tuple may be None.

    Examples of authority parsing:

    >>> _parse_proxy('proxy.example.com')
    (None, None, None, 'proxy.example.com')
    >>> _parse_proxy('proxy.example.com:3128')
    (None, None, None, 'proxy.example.com:3128')

    The authority component may optionally include userinfo (assumed to be
    username:password):

    >>> _parse_proxy('joe:password@proxy.example.com')
    (None, 'joe', 'password', 'proxy.example.com')
    >>> _parse_proxy('joe:password@proxy.example.com:3128')
    (None, 'joe', 'password', 'proxy.example.com:3128')

    Same examples, but with URLs instead:

    >>> _parse_proxy('http://proxy.example.com/')
    ('http', None, None, 'proxy.example.com')
    >>> _parse_proxy('http://proxy.example.com:3128/')
    ('http', None, None, 'proxy.example.com:3128')
    >>> _parse_proxy('http://joe:password@proxy.example.com/')
    ('http', 'joe', 'password', 'proxy.example.com')
    >>> _parse_proxy('http://joe:password@proxy.example.com:3128')
    ('http', 'joe', 'password', 'proxy.example.com:3128')

    Everything after the authority is ignored:

    >>> _parse_proxy('ftp://joe:password@proxy.example.com/rubbish:3128')
    ('ftp', 'joe', 'password', 'proxy.example.com')

    Test for no trailing '/' case:

    >>> _parse_proxy('http://joe:password@proxy.example.com')
    ('http', 'joe', 'password', 'proxy.example.com')

    """
    pass


class ProxyHandler(BaseHandler):
    # Proxies must be in front
    handler_order = 100

    def __init__(self, proxies=None, proxy_bypass=None):
        pass

    def proxy_open(self, req, proxy, type):
        pass

    def __copy__(self):
        return ProxyHandler(self.proxies.copy(), self._proxy_bypass)


class HTTPPasswordMgr:

    def __init__(self):
        self.passwd = {}

    def add_password(self, realm, uri, user, passwd):
        # uri could be a single URI or a sequence
        pass

    def find_user_password(self, realm, authuri):
        pass

    def reduce_uri(self, uri, default_port=True):
        """Accept authority or URI and extract only the authority and path."""
        pass

    def is_suburi(self, base, test):
        """Check if test is below base in a URI tree

        Both args must be URIs in reduced form.
        """
        pass

    def __copy__(self):
        ans = self.__class__()
        ans.passwd = copy.deepcopy(self.passwd)
        return ans


class HTTPPasswordMgrWithDefaultRealm(HTTPPasswordMgr):

    def find_user_password(self, realm, authuri):
        pass


class AbstractBasicAuthHandler:

    # XXX this allows for multiple auth-schemes, but will stupidly pick
    # the last one with a realm specified.

    # allow for double- and single-quoted realm values
    # (single quotes are a violation of the RFC, but appear in the wild)
    rx = re.compile('(?:^|,)'     # start of the string or ','
                    '[ \t]*'      # optional whitespaces
                    '([^ \t,]+)'  # scheme like "Basic"
                    '[ \t]+'      # mandatory whitespaces
                    # realm=xxx
                    # realm='xxx'
                    # realm="xxx"
                    'realm=(["\']?)([^"\']*)\\2',
                    re.I)

    # XXX could pre-emptively send auth info already accepted (RFC 2617,
    # end of section 2, and section 1.2 immediately after "credentials"
    # production).

    def __init__(self, password_mgr=None):
        pass

    def http_error_auth_reqed(self, authreq, host, req, headers):
        # host may be an authority (without userinfo) or a URL with an
        # authority
        # XXX could be multiple headers
        pass

    def retry_http_basic_auth(self, host, req, realm):
        pass

    def __copy__(self):
        return self.__class__(self.passwd.__copy__())


class HTTPBasicAuthHandler(AbstractBasicAuthHandler, BaseHandler):

    auth_header = 'Authorization'

    def http_error_401(self, req, fp, code, msg, headers):
        pass

    def __copy__(self):
        return AbstractBasicAuthHandler.__copy__(self)


class ProxyBasicAuthHandler(AbstractBasicAuthHandler, BaseHandler):

    auth_header = 'Proxy-authorization'

    def http_error_407(self, req, fp, code, msg, headers):
        # http_error_auth_reqed requires that there is no userinfo component in
        # authority.  Assume there isn't one, since urllib2 does not (and
        # should not, RFC 3986 s. 3.2.1) support requests for URLs containing
        # userinfo.
        pass

    def __copy__(self):
        return AbstractBasicAuthHandler.__copy__(self)


randombytes = os.urandom


class AbstractDigestAuthHandler:
    # Digest authentication is specified in RFC 2617.

    # XXX The client does not inspect the Authentication-Info header
    # in a successful response.

    # XXX It should be possible to test this implementation against
    # a mock server that just generates a static set of challenges.

    # XXX qop="auth-int" supports is shaky

    def __init__(self, passwd=None):
        pass

    def reset_retry_count(self):
        pass

    def http_error_auth_reqed(self, auth_header, host, req, headers):
        pass

    def retry_http_digest_auth(self, req, auth):
        pass

    def get_cnonce(self, nonce):
        # The cnonce-value is an opaque
        # quoted string value provided by the client and used by both client
        # and server to avoid chosen plaintext attacks, to provide mutual
        # authentication, and to provide some message integrity protection.
        # This isn't a fabulous effort, but it's probably Good Enough.
        pass

    def get_authorization(self, req, chal):
        pass

    def get_algorithm_impls(self, algorithm):
        # algorithm should be case-insensitive according to RFC2617
        pass

    def get_entity_digest(self, data, chal):
        # XXX not implemented yet
        pass

    def __copy__(self):
        return self.__class__(self.passwd.__copy__())


class HTTPDigestAuthHandler(BaseHandler, AbstractDigestAuthHandler):
    """An authentication protocol defined by RFC 2069

    Digest authentication improves on basic authentication because it
    does not transmit passwords in the clear.
    """

    auth_header = 'Authorization'
    handler_order = 490  # before Basic auth

    def http_error_401(self, req, fp, code, msg, headers):
        pass

    def __copy__(self):
        return AbstractDigestAuthHandler.__copy__(self)


class ProxyDigestAuthHandler(BaseHandler, AbstractDigestAuthHandler):

    auth_header = 'Proxy-Authorization'
    handler_order = 490  # before Basic auth

    def http_error_407(self, req, fp, code, msg, headers):
        pass

    def __copy__(self):
        return AbstractDigestAuthHandler.__copy__(self)


class AbstractHTTPHandler(BaseHandler):

    def __init__(self, debuglevel=0):
        self._debuglevel = debuglevel

    def set_http_debuglevel(self, level):
        pass

    def do_request_(self, request):
        pass

    def do_open(self, http_class, req):
        """Return an addinfourl object for the request, using http_class.

        http_class must implement the HTTPConnection API from httplib.
        The addinfourl return value is a file-like object.  It also
        has methods and attributes including:
            - info(): return a HTTPMessage object for the headers
            - geturl(): return the original request URL
            - code: HTTP status code
        """
        pass

    def __copy__(self):
        return self.__class__(self._debuglevel)


class HTTPHandler(AbstractHTTPHandler):

    def http_open(self, req):
        pass

    http_request = AbstractHTTPHandler.do_request_


class HTTPSHandler(AbstractHTTPHandler):

    def __init__(self, client_cert_manager=None):
        pass

    def https_open(self, req):
        pass

    https_request = AbstractHTTPHandler.do_request_

    def __copy__(self):
        ans = self.__class__(self.client_cert_manager)
        ans._debuglevel = self._debuglevel
        ans.ssl_context = self.ssl_context
        return ans


class HTTPCookieProcessor(BaseHandler):
    """Handle HTTP cookies.

    Public attributes:

    cookiejar: CookieJar instance

    """

    def __init__(self, cookiejar=None):
        pass

    def http_request(self, request):
        pass

    def http_response(self, request, response):
        pass

    def __copy__(self):
        return self.__class__(self.cookiejar)

    https_request = http_request
    https_response = http_response


class UnknownHandler(BaseHandler):

    def unknown_open(self, req):
        pass


def parse_keqv_list(ln):
    """Parse list of key=value strings where keys are not duplicated."""
    pass


def parse_http_list(s):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Neither commas nor quotes count if they are escaped.
    Only double-quotes count, not single-quotes.
    """
    pass


class FileHandler(BaseHandler):
    # Use local file or FTP depending on form of URL

    def file_open(self, req):
        pass

    # names for the localhost
    names = None

    def get_names(self):
        pass

    # not entirely sure what the rules are here
    def open_local_file(self, req):
        pass


class FTPHandler(BaseHandler):

    def ftp_open(self, req):
        pass

    def connect_ftp(self, user, passwd, host, port, dirs, timeout):
        pass


class CacheFTPHandler(FTPHandler):
    # XXX would be nice to have pluggable cache strategies
    # XXX this stuff is definitely not thread safe

    def __init__(self):
        self.cache = {}
        self.timeout = {}
        self.soonest = 0
        self.delay = 60
        self.max_conns = 16

    def setTimeout(self, t):
        pass

    def setMaxConns(self, m):
        pass

    def connect_ftp(self, user, passwd, host, port, dirs, timeout):
        pass

    def check_cache(self):
        # first check for old ones
        pass
