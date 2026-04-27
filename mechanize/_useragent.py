"""Convenient HTTP UserAgent class.

This is a subclass of urllib2.OpenerDirector.


Copyright 2003-2006 John J. Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it under
the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""

from __future__ import absolute_import

import copy

from . import _auth, _gzip, _opener, _response, _sockettimeout, _urllib2
from .polyglot import iteritems, itervalues


class UserAgentBase(_opener.OpenerDirector):
    """Convenient user-agent class.

    Do not use .add_handler() to add a handler for something already dealt with
    by this code.

    The only reason at present for the distinction between UserAgent and
    UserAgentBase is so that classes that depend on .seek()able responses
    (e.g. mechanize.Browser) can inherit from UserAgentBase.  The subclass
    UserAgent exposes a .set_seekable_responses() method that allows switching
    off the adding of a .seek() method to responses.

    Public attributes:

    addheaders: list of (name, value) pairs specifying headers to send with
     every request, unless they are overridden in the Request instance.

     >>> ua = UserAgentBase()
     >>> ua.addheaders = [
     ...  ("User-agent", "Mozilla/5.0 (compatible)"),
     ...  ("From", "responsible.person@example.com")]

    """

    handler_classes = {
        # scheme handlers
        "http": _urllib2.HTTPHandler,
        # CacheFTPHandler is buggy, at least in 2.3, so we don't use it
        "ftp": _urllib2.FTPHandler,
        "file": _urllib2.FileHandler,

        # other handlers
        "_unknown": _urllib2.UnknownHandler,
        # HTTP{S,}Handler depend on HTTPErrorProcessor too
        "_http_error": _urllib2.HTTPErrorProcessor,
        "_http_default_error": _urllib2.HTTPDefaultErrorHandler,

        # feature handlers
        "_basicauth": _urllib2.HTTPBasicAuthHandler,
        "_digestauth": _urllib2.HTTPDigestAuthHandler,
        "_redirect": _urllib2.HTTPRedirectHandler,
        "_cookies": _urllib2.HTTPCookieProcessor,
        "_refresh": _urllib2.HTTPRefreshProcessor,
        "_equiv": _urllib2.HTTPEquivProcessor,
        "_proxy": _urllib2.ProxyHandler,
        "_proxy_basicauth": _urllib2.ProxyBasicAuthHandler,
        "_proxy_digestauth": _urllib2.ProxyDigestAuthHandler,
        "_robots": _urllib2.HTTPRobotRulesProcessor,
        "_gzip": _gzip.HTTPGzipProcessor,

        # debug handlers
        "_debug_redirect": _urllib2.HTTPRedirectDebugProcessor,
        "_debug_response_body": _urllib2.HTTPResponseDebugProcessor,
    }

    default_schemes = ["http", "ftp", "file"]
    default_others = ["_unknown", "_http_error", "_http_default_error"]
    default_features = [
        "_gzip",
        "_redirect",
        "_cookies",
        "_refresh",
        "_equiv",
        "_basicauth",
        "_digestauth",
        "_proxy",
        "_proxy_basicauth",
        "_proxy_digestauth",
        "_robots",
    ]
    if hasattr(_urllib2, 'HTTPSHandler'):
        handler_classes["https"] = _urllib2.HTTPSHandler
        default_schemes.append("https")

    def __init__(self):
        pass

    def close(self):
        pass

# XXX
# def set_timeout(self, timeout):
#         self._timeout = timeout
# def set_http_connection_cache(self, conn_cache):
#         self._http_conn_cache = conn_cache
# def set_ftp_connection_cache(self, conn_cache):
# XXX ATM, FTP has cache as part of handler; should it be separate?
#         self._ftp_conn_cache = conn_cache

    def set_handled_schemes(self, schemes):
        """Set sequence of URL scheme (protocol) strings.

        For example: ua.set_handled_schemes(["http", "ftp"])

        If this fails (with ValueError) because you've passed an unknown
        scheme, the set of handled schemes will not be changed.

        """
        pass

    def set_cookiejar(self, cookiejar):
        """Set a mechanize.CookieJar, or None."""
        pass

    # XXX could use Greg Stein's httpx for some of this instead?
    # or httplib2??
    def set_proxies(self, proxies=None, proxy_bypass=None):
        """Configure proxy settings.

        :arg proxies: dictionary mapping URL scheme to proxy specification.
          None means use the default system-specific settings.
        :arg proxy_bypass: function taking hostname, returning whether proxy
          should be used.  None means use the default system-specific settings.

        The default is to try to obtain proxy settings from the system (see the
        documentation for urllib.urlopen for information about the
        system-specific methods used -- note that's urllib, not urllib2).

        To avoid all use of proxies, pass an empty proxies dict.

        >>> ua = UserAgentBase()
        >>> def proxy_bypass(hostname):
        ...     return hostname == "noproxy.com"
        >>> ua.set_proxies(
        ...     {"http": "joe:password@myproxy.example.com:3128",
        ...      "ftp": "proxy.example.com"},
        ...     proxy_bypass)

        """
        pass

    def add_password(self, url, user, password, realm=None):
        pass

    def add_proxy_password(self, user, password, hostport=None, realm=None):
        pass

    def add_client_certificate(self, url, key_file, cert_file):
        """Add an SSL client certificate, for HTTPS client auth.

        key_file and cert_file must be filenames of the key and certificate
        files, in PEM format.  You can use e.g. OpenSSL to convert a p12 (PKCS
        12) file to PEM format:

        openssl pkcs12 -clcerts -nokeys -in cert.p12 -out cert.pem
        openssl pkcs12 -nocerts -in cert.p12 -out key.pem


        Note that client certificate password input is very inflexible ATM.  At
        the moment this seems to be console only, which is presumably the
        default behaviour of libopenssl.  In future mechanize may support
        third-party libraries that (I assume) allow more options here.

        """
        pass

    # the following are rarely useful -- use add_password / add_proxy_password
    # instead
    def set_password_manager(self, password_manager):
        """Set a mechanize.HTTPPasswordMgrWithDefaultRealm, or None."""
        pass

    def set_proxy_password_manager(self, password_manager):
        """Set a mechanize.HTTPProxyPasswordMgr, or None."""
        pass

    def set_client_cert_manager(self, cert_manager):
        """Set a mechanize.HTTPClientCertMgr, or None."""
        pass

    def set_ca_data(self, cafile=None, capath=None, cadata=None, context=None):
        '''
        Set the SSL Context used for connecting to SSL servers.

        This method accepts the same arguments as the
        :py:meth:`ssl.SSLContext.load_verify_locations()` method from
        the Python standard library. You can also pass a pre-built
        :class:`ssl.SSLContext` via the `context` keyword argument.
        Note that to use this feature, you must be using Python >=
        2.7.9.

        '''
        pass

    # these methods all take a boolean parameter
    def set_handle_robots(self, handle):
        """Set whether to observe rules from robots.txt."""
        pass

    def set_handle_redirect(self, handle):
        """Set whether to handle HTTP 30x redirections."""
        pass

    def set_handle_refresh(self, handle, max_time=None, honor_time=True):
        """Set whether to handle HTTP Refresh headers."""
        pass

    def set_handle_equiv(self, handle, head_parser_class=None):
        """Set whether to treat HTML http-equiv headers like HTTP headers.

        Response objects may be .seek()able if this is set (currently returned
        responses are, raised HTTPError exception responses are not).

        """
        pass

    def set_request_gzip(self, handle):
        """Add header indicating to server that we handle gzip
        content encoding. Note that if the server sends gzip'ed content,
        it is handled automatically in any case, regardless of this setting.

        """
        pass
    set_handle_gzip = set_request_gzip  # legacy

    def set_debug_redirects(self, handle):
        """
        Log information about HTTP redirects (including refreshes).

        Logging is performed using module logging.  The logger name is
        `"mechanize.http_redirects"`.  To actually print some debug output,
        eg:

        .. code-block:: python

            import sys, logging
            logger = logging.getLogger("mechanize.http_redirects")
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.setLevel(logging.INFO)

        Other logger names relevant to this module:

        * `mechanize.http_responses`
        * `mechanize.cookies`

        To turn on everything:

        .. code-block:: python

            import sys, logging
            logger = logging.getLogger("mechanize")
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.setLevel(logging.INFO)

        """
        pass

    def set_debug_responses(self, handle):
        """Log HTTP response bodies.

        See :meth:`set_debug_redirects()` for details of logging.

        Response objects may be .seek()able if this is set (currently returned
        responses are, raised HTTPError exception responses are not).

        """
        pass

    def set_debug_http(self, handle):
        """Print HTTP headers to sys.stdout."""
        pass

    def _copy_state(self, other):
        pass

    def handlers_by_class(self, cls):
        pass

    def _set_handler(self,
                     name,
                     handle=None,
                     obj=None,
                     constructor_args=(),
                     constructor_kwds={}):
        pass

    def _replace_handler(self, name, newhandler=None):
        # first, if handler was previously added, remove it
        pass


class UserAgent(UserAgentBase):
    def __init__(self):
        pass

    def set_seekable_responses(self, handle):
        """Make response objects .seek()able."""
        pass

    def open(self,
             fullurl,
             data=None,
             timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        pass
