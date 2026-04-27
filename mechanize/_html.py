from __future__ import absolute_import

import codecs
import copy
import re

from ._form import parse_forms
from ._headersutil import is_html as _is_html
from ._headersutil import split_header_words
from ._rfc3986 import clean_url, urljoin
from .polyglot import is_string

DEFAULT_ENCODING = "utf-8"
_encoding_pats = (
    # XML declaration
    r'<\?[^<>]+encoding\s*=\s*[\'"](.*?)[\'"][^<>]*>',
    # HTML 5 charset
    r'''<meta\s+charset=['"]([-_a-z0-9]+)['"][^<>]*>(?:\s*</meta>){0,1}''',
    # HTML 4 Pragma directive
    r'''<meta\s+?[^<>]*?content\s*=\s*['"][^'"]*?charset=([-_a-z0-9]+)[^'"]*?['"][^<>]*>(?:\s*</meta>){0,1}''',
)


def compile_pats(binary):
    pass


class LazyEncodingPats(object):

    def __call__(self, binary=False):
        attr = 'binary_pats' if binary else 'unicode_pats'
        pats = getattr(self, attr, None)
        if pats is None:
            pats = tuple(compile_pats(binary))
            setattr(self, attr, pats)
        for pat in pats:
            yield pat


lazy_encoding_pats = LazyEncodingPats()


def find_declared_encoding(raw, limit=50*1024):
    pass


def elem_text(elem):
    pass


def iterlinks(root, base_url):
    pass


def compress_whitespace(text):
    pass


def get_encoding_from_response(response, verify=True):
    # HTTPEquivProcessor may be in use, so both HTTP and HTTP-EQUIV
    # headers may be in the response.  HTTP-EQUIV headers come last,
    # so try in order from first to last.
    pass


class EncodingFinder:
    def __init__(self, default_encoding):
        self._default_encoding = default_encoding

    def encoding(self, response):
        pass


class ResponseTypeFinder:
    def __init__(self, allow_xhtml):
        self._allow_xhtml = allow_xhtml

    def is_html(self, response, encoding):
        pass


class Link:
    '''
    A link in a HTML document

    :ivar absolute_url: The absolutized link URL
    :ivar url: The link URL
    :ivar base_url: The base URL against which this link is resolved
    :ivar text: The link text
    :ivar tag: The link tag name
    :ivar attrs: The tag attributes

    '''
    def __init__(self, base_url, url, text, tag, attrs):
        pass

    def __eq__(self, other):
        try:
            for name in "url", "text", "tag":
                if getattr(self, name) != getattr(other, name):
                    return False
            if dict(self.attrs) != dict(other.attrs):
                return False
        except AttributeError:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Link(base_url=%r, url=%r, text=%r, tag=%r, attrs=%r)" % (
            self.base_url, self.url, self.text, self.tag, self.attrs)


def content_parser(data,
                   url=None,
                   response_info=None,
                   transport_encoding=None,
                   default_encoding=DEFAULT_ENCODING,
                   is_html=True):
    '''
    Parse data (a bytes object) into an etree representation such as
    :py:mod:`xml.etree.ElementTree` or `lxml.etree`

    :param bytes data: The data to parse
    :param url: The URL of the document being parsed or None
    :param response_info: Information about the document
        (contains all HTTP headers as :class:`HTTPMessage`)
    :param transport_encoding: The character encoding for the document being
        parsed as specified in the HTTP headers or None.
    :param default_encoding: The character encoding to use if no encoding
        could be detected and no transport_encoding is specified
    :param is_html: If the document is to be parsed as HTML.
    '''
    pass


def get_title(root):
    pass


lazy = object()


class Factory:
    """Factory for forms, links, etc.

    This interface may expand in future.

    Public methods:

    set_request_class(request_class)
    set_response(response)
    forms()
    links()

    Public attributes:

    Note that accessing these attributes may raise ParseError.

    encoding: string specifying the encoding of response if it contains a text
     document (this value is left unspecified for documents that do not have
     an encoding, e.g. an image file)
    is_html: true if response contains an HTML document (XHTML may be
     regarded as HTML too)
    title: page title, or None if no title or not HTML
    global_form: form object containing all controls that are not descendants
     of any FORM element, or None if the forms_factory does not support
     supplying a global form

    """

    def __init__(
            self,
            default_encoding=DEFAULT_ENCODING,
            allow_xhtml=False, ):
        """

        Pass keyword arguments only.

        """
        pass

    def set_content_parser(self, val):
        pass

    def set_request_class(self, request_class):
        """Set request class (mechanize.Request by default).

        HTMLForm instances returned by .forms() will return instances of this
        class when .click()ed.

        """
        pass

    def set_response(self, response):
        """Set response.

        The response must either be None or implement the same interface as
        objects returned by mechanize.urlopen().

        """
        pass

    @property
    def root(self):
        pass

    @property
    def title(self):
        pass

    @property
    def global_form(self):
        pass

    def forms(self):
        """ Return tuple of HTMLForm-like objects. """
        pass

    def links(self):
        """Return tuple of mechanize.Link-like objects.  """
        pass

    def _get_links(self):
        pass

    def _get_forms(self):
        pass
