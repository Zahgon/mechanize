"""HTTP Authentication and Proxy support.


Copyright 2006 John J. Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it under
the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""

from __future__ import absolute_import
from ._urllib2_fork import HTTPPasswordMgr
from .polyglot import is_string, iteritems


# TODO: stop deriving from HTTPPasswordMgr
class HTTPProxyPasswordMgr(HTTPPasswordMgr):
    # has default realm and host/port

    def add_password(self, realm, uri, user, passwd):
        # uri could be a single URI or a sequence
        pass

    def find_user_password(self, realm, authuri):
        pass

    def reduce_uri(self, uri, default_port=True):
        pass

    def is_suburi(self, base, test):
        pass


class HTTPSClientCertMgr(HTTPPasswordMgr):
    # implementation inheritance: this is not a proper subclass

    def add_key_cert(self, uri, key_file, cert_file):
        pass

    def find_key_cert(self, authuri):
        pass
