"""Response classes.

The seek_wrapper code is not used if you're using UserAgent with
.set_seekable_responses(False), or if you're using the urllib2-level interface
HTTPEquivProcessor.  Class closeable_response is instantiated by some handlers
(AbstractHTTPHandler), but the closeable_response interface is only depended
upon by Browser-level code.  Function upgrade_response is only used if you're
using Browser.


Copyright 2006 John J. Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""

from __future__ import absolute_import
from functools import partial
import copy
from io import BytesIO

from ._headersutil import normalize_header_name
from .polyglot import HTTPError, create_response_info


def len_of_seekable(file_):
    # this function exists because evaluation of len(file_.getvalue()) on every
    # .read() from seek_wrapper would be O(N**2) in number of .read()s
    pass


# XXX Andrew Dalke kindly sent me a similar class in response to my request on
# comp.lang.python, which I then proceeded to lose.  I wrote this class
# instead, but I think he's released his code publicly since, could pinch the
# tests from it, at least...


# For testing seek_wrapper invariant (note that
# test_urllib2.HandlerTest.test_seekable is expected to fail when this
# invariant checking is turned on).  The invariant checking is done by module
# ipdc, which is available here:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/436834
# from ipdbc import ContractBase
# class seek_wrapper(ContractBase):
class seek_wrapper:
    """Adds a seek method to a file object.

    This is only designed for seeking on readonly file-like objects.

    Wrapped file-like object must have a read method.  The readline method is
    only supported if that method is present on the wrapped object.  The
    readlines method is always supported.  xreadlines and iteration are
    supported only for Python 2.2 and above.

    Public attributes:

    wrapped: the wrapped file object
    is_closed: true iff .close() has been called

    WARNING: All other attributes of the wrapped object (ie. those that are not
    one of wrapped, read, readline, readlines, xreadlines, __iter__ and next)
    are passed through unaltered, which may or may not make sense for your
    particular file object.

    """

    # General strategy is to check that cache is full enough, then delegate to
    # the cache (self.__cache, which is a BytesIO instance).  A seek
    # position (self.__pos) is maintained independently of the cache, in order
    # that a single cache may be shared between multiple seek_wrapper objects.
    # Copying using module copy shares the cache in this way.

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.__read_complete_state = [False]
        self.__is_closed_state = [False]
        self.__have_readline = hasattr(self.wrapped, "readline")
        self.__cache = BytesIO()
        self.__pos = 0  # seek position

    def invariant(self):
        # The end of the cache is always at the same place as the end of the
        # wrapped file (though the .tell() method is not required to be present
        # on wrapped file).
        pass

    def close(self):
        pass

    def __getattr__(self, name):
        if name == "is_closed":
            return self.__is_closed_state[0]
        elif name == "read_complete":
            return self.__read_complete_state[0]

        wrapped = self.__dict__.get("wrapped")
        if wrapped:
            return getattr(wrapped, name)

        return getattr(self.__class__, name)

    def __setattr__(self, name, value):
        if name == "is_closed":
            self.__is_closed_state[0] = bool(value)
        elif name == "read_complete":
            if not self.is_closed:
                self.__read_complete_state[0] = bool(value)
        else:
            self.__dict__[name] = value

    def seek(self, offset, whence=0):
        pass

    def tell(self):
        pass

    def __copy__(self):
        cpy = self.__class__(self.wrapped)
        cpy.__cache = self.__cache
        cpy.__read_complete_state = self.__read_complete_state
        cpy.__is_closed_state = self.__is_closed_state
        return cpy

    def get_data(self):
        pass

    def read(self, size=-1):
        pass

    def readline(self, size=-1):
        pass

    def readlines(self, sizehint=-1):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    next = __next__

    xreadlines = __iter__

    def __repr__(self):
        return "<%s at %s whose wrapped object = %r>" % (
            self.__class__.__name__,
            hex(abs(id(self))),
            self.wrapped,
        )


class response_seek_wrapper(seek_wrapper):
    """
    Supports copying response objects and setting response body data.

    """

    def __init__(self, wrapped):
        pass

    def __copy__(self):
        cpy = seek_wrapper.__copy__(self)
        # copy headers from delegate
        cpy._headers = copy.copy(self.info())
        return cpy

    # Note that .info() and .geturl() (the only two urllib2 response methods
    # that are not implemented by seek_wrapper) must be here explicitly rather
    # than by seek_wrapper's __getattr__ delegation) so that the nasty
    # dynamically-created HTTPError classes in get_seek_wrapper_class() get the
    # wrapped object's implementation, and not HTTPError's.

    def info(self):
        pass

    @property
    def headers(self):
        pass

    def geturl(self):
        pass

    def set_data(self, data):
        pass


class eoffile:
    # file-like object that always claims to be at end-of-file...

    def read(self, size=-1):
        pass

    def readline(self, size=-1):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return b""

    next = __next__

    def close(self):
        pass


class eofresponse(eoffile):
    def __init__(self, url, headers, code, msg):
        self._url = url
        self._headers = headers
        self.code = code
        self.msg = msg

    def geturl(self):
        pass

    def info(self):
        pass

    @property
    def headers(self):
        pass


class closeable_response:
    """Avoids unnecessarily clobbering urllib.addinfourl methods on .close().

    Only supports responses returned by mechanize.HTTPHandler.

    After .close(), the following methods are supported:

    .read()
    .readline()
    .info()
    .geturl()
    .__iter__()
    .next()
    .close()

    and the following attributes are supported:

    .code
    .msg
    .http_version

    Also supports pickling (but the stdlib currently does something to prevent
    it: http://python.org/sf/1144636).

    """

    # presence of this attr indicates is useable after .close()
    closeable_response = None

    def __init__(self, fp, headers, url, code=200, msg="OK", http_version=None):
        pass

    def _set_fp(self, fp):
        pass

    def __repr__(self):
        return "<%s at %s whose fp = %r>" % (
            self.__class__.__name__,
            hex(abs(id(self))),
            self.fp,
        )

    def info(self):
        pass

    @property
    def headers(self):
        pass

    def getcode(self):
        pass

    def get_header_values(self, name):
        pass

    def get_all_header_names(self, normalize=True):
        pass

    def __getitem__(self, name):
        return self._headers[name]

    def get(self, name, default):
        pass

    def geturl(self):
        pass

    def close(self):
        pass


def test_response(data="test data", headers=(), url=None, code=200, msg="OK"):
    pass


_html_header = [("Content-type", "text/html")]


def test_html_response(data="test data", headers=(), url=None, code=200, msg="OK"):
    pass


def make_response(data, headers, url=None, code=200, msg="OK"):
    """Convenient factory for objects implementing response interface.

    data: string containing response body data
    headers: sequence of (name, value) pairs
    url: URL of response
    code: integer response code (e.g. 200)
    msg: string response code message (e.g. "OK")

    """
    pass


def make_headers(headers):
    """
    headers: sequence of (name, value) pairs
    """
    pass


# Rest of this module is especially horrible, but needed, at least until fork
# urllib2.  Even then, may want to preseve urllib2 compatibility.


def get_seek_wrapper_class(response):
    # in order to wrap response objects that are also exceptions, we must
    # dynamically subclass the exception :-(((
    pass
    pass


def needs_seek_wrapper(obj):
    pass


def seek_wrapped_response(response):
    """Return a copy of response that supports seekable response interface.

    Accepts responses from both mechanize and urllib2 handlers.

    Copes with both ordinary response instances and HTTPError instances (which
    can't be simply wrapped due to the requirement of preserving the exception
    base class).
    """
    pass


def upgrade_response(response):
    """Return a copy of response that supports Browser response interface.

    Browser response interface is that of "seekable responses"
    (response_seek_wrapper), plus the requirement that responses must be
    useable after .close() (closeable_response).

    Accepts responses from both mechanize and urllib2 handlers.

    Copes with both ordinary response instances and HTTPError instances (which
    can't be simply wrapped due to the requirement of preserving the exception
    base class).
    """
    pass
