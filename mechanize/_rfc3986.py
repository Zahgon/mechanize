"""RFC 3986 URI parsing and relative reference resolution / absolutization.

(aka splitting and joining)

Copyright 2006 John J. Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it under
the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""

# XXX Wow, this is ugly.  Overly-direct translation of the RFC ATM.

from __future__ import absolute_import
import re

from .polyglot import quote
# def chr_range(a, b):
# return "".join(map(chr, range(ord(a), ord(b)+1)))

# UNRESERVED_URI_CHARS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# "abcdefghijklmnopqrstuvwxyz"
# "0123456789"
# "-_.~")
# RESERVED_URI_CHARS = "!*'();:@&=+$,/?#[]"
# URI_CHARS = RESERVED_URI_CHARS+UNRESERVED_URI_CHARS+'%'
# this re matches any character that's not in URI_CHARS
BAD_URI_CHARS_RE = re.compile(r"[^A-Za-z0-9\-_.~!*'();:@&=+$,/?%#[\]]")


def clean_url(url, encoding='utf-8'):
    # percent-encode illegal URI characters
    # Trying to come up with test cases for this gave me a headache, revisit
    # when do switch to unicode.
    # Somebody else's comments (lost the attribution):
    # - IE will return you the url in the encoding you send it
    # - Mozilla/Firefox will send you latin-1 if there's no non latin-1
    # characters in your link. It will send you utf-8 however if there are...
    pass


def is_clean_uri(uri):
    """
    >>> is_clean_uri("ABC!")
    True
    >>> is_clean_uri(u"ABC!")
    True
    >>> is_clean_uri("ABC|")
    False
    >>> is_clean_uri(u"ABC|")
    False
    >>> is_clean_uri("http://example.com/0")
    True
    >>> is_clean_uri(u"http://example.com/0")
    True
    """
    pass


SPLIT_MATCH = re.compile(
    r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?").match


def urlsplit(absolute_uri):
    """Return scheme, authority, path, query, fragment."""
    pass


def urlunsplit(parts):
    pass


def urljoin(base_uri, uri_reference):
    """Join a base URI with a URI reference and return the resulting URI.

    See RFC 3986.
    """
    pass

# oops, this doesn't do the same thing as the literal translation
# from the RFC below
# import posixpath
# def urljoin_parts(base_parts, reference_parts):
#     scheme, authority, path, query, fragment = base_parts
#     rscheme, rauthority, rpath, rquery, rfragment = reference_parts

# compute target URI path
# if rpath == "":
#         tpath = path
# else:
#         tpath = rpath
# if not tpath.startswith("/"):
#             tpath = merge(authority, path, tpath)
#         tpath = posixpath.normpath(tpath)

# if rscheme is not None:
# return (rscheme, rauthority, tpath, rquery, rfragment)
# elif rauthority is not None:
# return (scheme, rauthority, tpath, rquery, rfragment)
# elif rpath == "":
# if rquery is not None:
#             tquery = rquery
# else:
#             tquery = query
# return (scheme, authority, tpath, tquery, rfragment)
# else:
# return (scheme, authority, tpath, rquery, rfragment)


def urljoin_parts(base_parts, reference_parts):
    pass

# um, something *vaguely* like this is what I want, but I have to generate
# lots of test cases first, if only to understand what it is that
# remove_dot_segments really does...
# def remove_dot_segments(path):
# if path == '':
# return ''
#     comps = path.split('/')
#     new_comps = []
# for comp in comps:
# if comp in ['.', '']:
# if not new_comps or new_comps[-1]:
# new_comps.append('')
# continue
# if comp != '..':
# new_comps.append(comp)
# elif new_comps:
# new_comps.pop()
# return '/'.join(new_comps)


def remove_dot_segments(path):
    pass


def merge(base_authority, base_path, ref_path):
    # XXXX Oddly, the sample Perl implementation of this by Roy Fielding
    # doesn't even take base_authority as a parameter, despite the wording in
    # the RFC suggesting otherwise.  Perhaps I'm missing some obvious identity.
    # if base_authority is not None and base_path == "":
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
