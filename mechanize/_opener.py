"""URL opener.

Copyright 2004-2006 John J Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file
LICENSE included with the distribution).

"""

from __future__ import absolute_import

import bisect
import os
import tempfile
import threading

from . import _response
from . import _rfc3986
from . import _sockettimeout
from . import _urllib2_fork
from ._request import Request
from ._util import isstringlike
from .polyglot import HTTPError, URLError, iteritems, is_class


open_file = open


class ContentTooShortError(URLError):

    def __init__(self, reason, result):
        pass


def set_request_attr(req, name, value, default):
    pass


class OpenerDirector(_urllib2_fork.OpenerDirector):

    def __init__(self):
        pass

    def add_handler(self, handler):
        pass

    def _maybe_reindex_handlers(self):
        pass

    def _request(self, url_or_req, data, visit,
                 timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        pass

    def open(self, fullurl, data=None,
             timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        pass

    def error(self, proto, *args):
        pass

    BLOCK_SIZE = 1024 * 8

    def retrieve(self, fullurl, filename=None, reporthook=None, data=None,
                 timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT,
                 open=open_file):
        """Returns (filename, headers).

        For remote objects, the default filename will refer to a temporary
        file.  Temporary files are removed when the OpenerDirector.close()
        method is called.

        For file: URLs, at present the returned filename is None.  This may
        change in future.

        If the actual number of bytes read is less than indicated by the
        Content-Length header, raises ContentTooShortError (a URLError
        subclass).  The exception's .result attribute contains the (filename,
        headers) that would have been returned.

        """
        pass

    def close(self):
        pass


def wrapped_open(urlopen, process_response_object, fullurl, data=None,
                 timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    pass


class ResponseProcessingOpener(OpenerDirector):

    def open(self, fullurl, data=None,
             timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        pass

    def process_response_object(self, response):
        pass


class SeekableResponseOpener(ResponseProcessingOpener):

    def process_response_object(self, response):
        pass


class OpenerFactory:
    """This class's interface is quite likely to change."""

    default_classes = [
        # handlers
        _urllib2_fork.ProxyHandler,
        _urllib2_fork.UnknownHandler,
        _urllib2_fork.HTTPHandler,
        _urllib2_fork.HTTPDefaultErrorHandler,
        _urllib2_fork.HTTPRedirectHandler,
        _urllib2_fork.FTPHandler,
        _urllib2_fork.FileHandler,
        # processors
        _urllib2_fork.HTTPCookieProcessor,
        _urllib2_fork.HTTPErrorProcessor,
    ]
    default_classes.append(_urllib2_fork.HTTPSHandler)
    handlers = []
    replacement_handlers = []

    def __init__(self, klass=OpenerDirector):
        self.klass = klass

    def build_opener(self, *handlers):
        """Create an opener object from a list of handlers and processors.

        The opener will use several default handlers and processors, including
        support for HTTP and FTP.

        If any of the handlers passed as arguments are subclasses of the
        default handlers, the default handlers will not be used.

        """
        pass


build_opener = OpenerFactory().build_opener

thread_local = threading.local()
thread_local.opener = None


def get_thread_local_opener():
    pass


def urlopen(url, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    pass


def urlretrieve(url, filename=None, reporthook=None, data=None,
                timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    pass


def install_opener(opener):
    pass
