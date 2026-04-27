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
        URLError.__init__(self, reason)
        self.result = result


def set_request_attr(req, name, value, default):
    try:
        getattr(req, name)
    except AttributeError:
        setattr(req, name, default)
    if value is not default:
        setattr(req, name, value)


class OpenerDirector(_urllib2_fork.OpenerDirector):

    def __init__(self):
        _urllib2_fork.OpenerDirector.__init__(self)
        # really none of these are (sanely) public -- the lack of initial
        # underscore on some is just due to following urllib2
        self.process_response = {}
        self.process_request = {}
        self._any_request = {}
        self._any_response = {}
        self._handler_index_valid = True
        self._tempfiles = []

    def add_handler(self, handler):
        if not hasattr(handler, "add_parent"):
            raise TypeError("expected BaseHandler instance, got %r" %
                            type(handler))

        if handler in self.handlers:
            return
        # XXX why does self.handlers need to be sorted?
        bisect.insort(self.handlers, handler)
        handler.add_parent(self)
        self._handler_index_valid = False

    def _maybe_reindex_handlers(self):
        pass

    def _request(self, url_or_req, data, visit,
                 timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        if isstringlike(url_or_req):
            req = Request(url_or_req, data, visit=visit, timeout=timeout)
        else:
            # already a mechanize.Request instance
            req = url_or_req
            if data is not None:
                req.add_data(data)
            # XXX yuck
            set_request_attr(req, "visit", visit, None)
            set_request_attr(req, "timeout", timeout,
                             _sockettimeout._GLOBAL_DEFAULT_TIMEOUT)
        return req

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
        req = self._request(fullurl, data, False, timeout)
        scheme = req.get_type()
        fp = self.open(req)
        try:
            headers = fp.info()
            if filename is None and scheme == 'file':
                # XXX req.get_selector() seems broken here, return None,
                #   pending sanity :-/
                return None, headers
                # return urllib.url2pathname(req.get_selector()), headers
            if filename:
                tfp = open(filename, 'wb')
            else:
                path = _rfc3986.urlsplit(req.get_full_url())[2]
                suffix = os.path.splitext(path)[1]
                fd, filename = tempfile.mkstemp(suffix)
                self._tempfiles.append(filename)
                tfp = os.fdopen(fd, 'wb')
            try:
                result = filename, headers
                bs = self.BLOCK_SIZE
                size = -1
                read = 0
                blocknum = 0
                if reporthook:
                    if "content-length" in headers:
                        size = int(headers["content-length"])
                    reporthook(blocknum, bs, size)
                while 1:
                    block = fp.read(bs)
                    if not block:
                        break
                    read += len(block)
                    tfp.write(block)
                    blocknum += 1
                    if reporthook:
                        reporthook(blocknum, bs, size)
            finally:
                tfp.close()
        finally:
            fp.close()

        # raise exception if actual size does not match content-length header
        if size >= 0 and read < size:
            raise ContentTooShortError(
                "retrieval incomplete: "
                "got only %i out of %i bytes" % (read, size),
                result
            )

        return result

    def close(self):
        _urllib2_fork.OpenerDirector.close(self)

        # make it very obvious this object is no longer supposed to be used
        self.open = self.error = self.retrieve = self.add_handler = None

        if self._tempfiles:
            for filename in self._tempfiles:
                try:
                    os.unlink(filename)
                except OSError:
                    pass
            del self._tempfiles[:]


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
        opener = self.klass()
        default_classes = list(self.default_classes)
        skip = set()
        for klass in default_classes:
            for check in handlers:
                if is_class(check):
                    if issubclass(check, klass):
                        skip.add(klass)
                elif isinstance(check, klass):
                    skip.add(klass)
        for klass in skip:
            default_classes.remove(klass)

        for klass in default_classes:
            opener.add_handler(klass())
        for h in handlers:
            if is_class(h):
                h = h()
            opener.add_handler(h)

        return opener


build_opener = OpenerFactory().build_opener

thread_local = threading.local()
thread_local.opener = None


def get_thread_local_opener():
    try:
        ans = thread_local.opener
    except AttributeError:
        # threading module is broken, use a single global instance
        ans = getattr(get_thread_local_opener, 'ans', None)
        if ans is None:
            ans = get_thread_local_opener.ans = build_opener()
    if ans is None:
        ans = thread_local.opener = build_opener()
    return ans


def urlopen(url, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    return get_thread_local_opener().open(url, data, timeout)


def urlretrieve(url, filename=None, reporthook=None, data=None,
                timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    return get_thread_local_opener().retrieve(
        url, filename, reporthook, data, timeout)


def install_opener(opener):
    get_thread_local_opener.ans = opener
    try:
        thread_local.opener = opener
    except AttributeError:
        pass
