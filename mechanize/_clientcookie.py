from __future__ import absolute_import

import re
import time
from .polyglot import (
    Cookie as _Cookie, CookieJar as CJ, MozillaCookieJar as MCJ, request_host
    as request_host_lc, DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
    FileCookieJar, LoadError, LWPCookieJar, _debug, domain_match,
    eff_request_host, escape_path, is_HDN, lwp_cookie_str, reach, request_path,
    request_port, user_domain_match, iteritems)

__all__ = [
    'DEFAULT_HTTP_PORT', 'CookiePolicy', 'DefaultCookiePolicy',
    'request_host_lc', 'MozillaCookieJar', 'escape_path', 'is_HDN',
    'request_port', 'LWPCookieJar', 'LoadError', 'reach', 'FileCookieJar',
    'lwp_cookie_str', 'domain_match', 'request_path', 'user_domain_match'
]


def effective_request_host(request):
    """Return the effective request-host, as defined by RFC 2965."""
    pass


def request_is_unverifiable(request):
    pass


def cookies_equal(a, b):
    pass


class Cookie(_Cookie):
    _attrs = ("version", "name", "value", "port", "port_specified", "domain",
              "domain_specified", "domain_initial_dot", "path",
              "path_specified", "secure", "expires", "discard", "comment",
              "comment_url", "rfc2109", "_rest")

    def __eq__(self, other):
        return all(getattr(self, a) == getattr(other, a) for a in self._attrs)

    def __ne__(self, other):
        return not (self == other)


class CookieJar(CJ):

    def __getstate__(self):
        ans = self.__dict__.copy()
        del ans['_cookies_lock']
        return ans

    def __setstate__(self, val):
        for k, v in iteritems(val):
            setattr(self, k, v)

    def cookies_for_request(self, request):
        """Return a list of cookies to be returned to server.

        The returned list of cookie instances is sorted in the order they
        should appear in the Cookie: header for return to the server.

        See add_cookie_header.__doc__ for the interface required of the
        request argument.
        """
        pass

    def get_policy(self):
        pass

    def _normalized_cookie_tuples(self, attrs_set):
        """Return list of tuples containing normalised cookie information.

        attrs_set is the list of lists of key,value pairs extracted from
        the Set-Cookie or Set-Cookie2 headers.

        Tuples are name, value, standard, rest, where name and value are the
        cookie name and value, standard is a dictionary containing the standard
        cookie-attributes (discard, secure, version, expires or max-age,
        domain, path and port) and rest is a dictionary containing the rest of
        the cookie-attributes.

        """
        pass

    def __getitem__(self, i):
        for q, ans in enumerate(self):
            if q == i:
                return ans
        raise IndexError()


try:
    from http.cookiejar import NETSCAPE_MAGIC_RGX, NETSCAPE_HEADER_TEXT
except ImportError:  # python < 3.10
    NETSCAPE_MAGIC_RGX = MCJ.magic_re
    NETSCAPE_HEADER_TEXT = MCJ.header
else:
    MCJ.header = NETSCAPE_HEADER_TEXT  # needed for tests


class MozillaCookieJar(MCJ):

    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        pass
