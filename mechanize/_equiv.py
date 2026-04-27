#!/usr/bin/env python
# vim:fileencoding=utf-8
# Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import re
import string

from ._entities import html5_entities
from .polyglot import codepoint_to_chr

space_chars = frozenset(("\t", "\n", "\u000C", " ", "\r"))
space_chars_bytes = frozenset(item.encode("ascii") for item in space_chars)
ascii_letters_bytes = frozenset(
    item.encode("ascii") for item in string.ascii_letters)
spaces_angle_brackets = space_chars_bytes | frozenset((b">", b"<"))
skip1 = space_chars_bytes | frozenset((b"/", ))
head_elems = frozenset((
    b"html", b"head", b"title", b"base", b"script",
    b"style", b"meta", b"link", b"object"))


def my_unichr(num):
    pass


def replace_entity(match):
    pass


class Bytes(bytes):
    """String-like object with an associated position and various extra methods
    If the position is ever greater than the string length then an exception is
    raised"""

    def __init__(self, value):
        self._position = -1

    def __iter__(self):
        return self

    def __next__(self):
        p = self._position = self._position + 1
        if p >= len(self):
            raise StopIteration
        elif p < 0:
            raise TypeError
        return self[p:p + 1]

    def next(self):
        # Py2 compat
        pass

    def previous(self):
        pass

    @property
    def position(self):
        pass

    @position.setter
    def position(self, position):
        pass

    @property
    def current_byte(self):
        pass

    def skip(self, chars=space_chars_bytes):
        """Skip past a list of characters"""
        pass

    def skip_until(self, chars):
        pass

    def match_bytes(self, bytes):
        """Look for a sequence of bytes at the start of a string. If the bytes
        are found return True and advance the position to the byte after the
        match. Otherwise return False and leave the position alone"""
        pass

    def match_bytes_pat(self, pat):
        pass

    def jump_to(self, bytes):
        """Look for the next sequence of bytes matching a given sequence. If
        a match is found advance the position to the last byte of the match"""
        pass


class HTTPEquivParser(object):
    """Mini parser for detecting http-equiv headers from meta tags """

    def __init__(self, data):
        """string - the data to work on """
        self.data = Bytes(data)
        self.headers = []

    def __call__(self):
        mb, mbp = self.data.match_bytes, self.data.match_bytes_pat
        dispatch = (
                (mb, b"<!--", self.handle_comment),
                (mbp, re.compile(b"<meta", flags=re.IGNORECASE),
                    self.handle_meta),
                (mbp, re.compile(b"</head", flags=re.IGNORECASE),
                    lambda: False),
                (mb, b"</", self.handle_possible_end_tag),
                (mb, b"<!", self.handle_other),
                (mb, b"<?", self.handle_other),
                (mb, b"<", self.handle_possible_start_tag)
        )
        for byte in self.data:
            keep_parsing = True
            for matcher, key, method in dispatch:
                if matcher(key):
                    try:
                        keep_parsing = method()
                        break
                    except StopIteration:
                        keep_parsing = False
                        break
            if not keep_parsing:
                break

        ans = []
        entity_pat = re.compile(r'&(\S+?);')
        for name, val in self.headers:
            try:
                name, val = name.decode('ascii'), val.decode('ascii')
            except ValueError:
                continue
            name = entity_pat.sub(replace_entity, name)
            val = entity_pat.sub(replace_entity, val)
            try:
                name, val = name.encode('ascii'), val.encode('ascii')
            except ValueError:
                continue
            ans.append((name, val))
        return ans

    def handle_comment(self):
        """Skip over comments"""
        pass

    def handle_meta(self):
        pass

    def handle_possible_start_tag(self):
        pass

    def handle_possible_end_tag(self):
        pass

    def handle_possible_tag(self, end_tag):
        pass

    def handle_other(self):
        pass

    def get_attribute(self):
        """Return a name,value pair for the next attribute in the stream,
        if one is found, or None"""
        pass
