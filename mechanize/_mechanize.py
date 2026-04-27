"""Stateful programmatic WWW navigation, after Perl's WWW::Mechanize.

Copyright 2003-2006 John J. Lee <jjl@pobox.com>
Copyright 2003 Andy Lester (original Perl code)

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""
from __future__ import absolute_import

import copy
import os
import re

from . import _request, _response, _rfc3986, _sockettimeout, _urllib2_fork
from ._clientcookie import Cookie
from ._headersutil import normalize_header_name
from ._html import Factory
from ._useragent import UserAgentBase
from .polyglot import pathname2url, HTTPError, is_string, iteritems
from ._response import make_response


class BrowserStateError(Exception):
    pass


class LinkNotFoundError(Exception):
    pass


class FormNotFoundError(Exception):
    pass


def sanepathname2url(path):
    pass


class History:
    """

    Though this will become public, the implied interface is not yet stable.

    """

    def __init__(self):
        self._history = []  # LIFO

    def add(self, request, response):
        pass

    def back(self, n, _response):
        pass

    def clear(self):
        pass

    def close(self):
        pass

    def __copy__(self):
        ans = self.__class__()
        ans._history = self._history[:]
        return ans


class HTTPRefererProcessor(_urllib2_fork.BaseHandler):
    def http_request(self, request):
        # See RFC 2616 14.36.  The only times we know the source of the
        # request URI has a URI associated with it are redirect, and
        # Browser.click() / Browser.submit() / Browser.follow_link().
        # Otherwise, it's the user's job to add any Referer header before
        # .open()ing.
        pass

    https_request = http_request


class Browser(UserAgentBase):
    """Browser-like class with support for history, forms and links.

    :class:`BrowserStateError` is raised whenever the browser is in the wrong
    state to complete the requested operation - e.g., when :meth:`back()` is
    called when the browser history is empty, or when :meth:`follow_link()` is
    called when the current response does not contain HTML data.

    Public attributes:

    request: current request (:class:`mechanize.Request`)

    form: currently selected form (see :meth:`select_form()`)

    :param history: object implementing the :class:`mechanize.History`
                    interface.  Note this interface is still experimental
                    and may change in future. This object is owned
                    by the browser instance and must not be shared
                    among browsers.
    :param request_class: Request class to use. Defaults to
                            :class:`mechanize.Request`
    :param content_parser: A function that is responsible for parsing
        received html/xhtml content. See the builtin
        :func:`mechanize._html.content_parser()` function for details
        on the interface this function must support.
    :param factory_class: HTML Factory class to use. Defaults to
                            :class:`mechanize.Factory`

    """

    handler_classes = copy.copy(UserAgentBase.handler_classes)
    handler_classes["_referer"] = HTTPRefererProcessor
    default_features = copy.copy(UserAgentBase.default_features)
    default_features.append("_referer")

    def __init__(
            self,
            history=None,
            request_class=None,
            content_parser=None,
            factory_class=Factory,
            allow_xhtml=False, ):
        """
        Only named arguments should be passed to this constructor.

        """
        pass

    def __copy__(self):
        '''
        Clone this browser instance. The clone will share the same, thread-safe
        cookie jar, and have all the same handlers/settings, but will not share
        any other state, making it safe to use in another thread.
        '''
        ans = self.__class__()
        self._copy_state(ans)
        ans._handle_referer = self._handle_referer
        for attr in ('_response_type_finder', '_encoding_finder',
                     '_content_parser'):
            setattr(ans._factory, attr, getattr(self._factory, attr))
        ans.request_class = self.request_class
        ans._history = copy.copy(self._history)
        return ans

    def close(self):
        pass

    def set_handle_referer(self, handle):
        """Set whether to add Referer header to each request."""
        pass

    def _add_referer_header(self, request, origin_request=True):
        pass

    def open_novisit(self,
                     url_or_request,
                     data=None,
                     timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        """Open a URL without visiting it.

        Browser state (including request, response, history, forms and links)
        is left unchanged by calling this function.

        The interface is the same as for :meth:`open()`.

        This is useful for things like fetching images.

        See also :meth:`retrieve()`

        """
        pass

    def open(self,
             url_or_request,
             data=None,
             timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        '''
        Open a URL. Loads the page so that you can subsequently use
        :meth:`forms()`, :meth:`links()`, etc. on it.

        :param url_or_request: Either a URL or a :class:`mechanize.Request`
        :param dict data: data to send with a POST request
        :param timeout: Timeout in seconds
        :return: A :class:`mechanize.Response` object
        '''
        pass

    def _mech_open(self,
                   url,
                   data=None,
                   update_history=True,
                   visit=None,
                   timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        pass

    def __str__(self):
        text = []
        text.append("<%s " % self.__class__.__name__)
        if self._response:
            text.append("visiting %s" % self._response.geturl())
        else:
            text.append("(not visiting a URL)")
        if self.form:
            text.append("\n selected form:\n %s\n" % str(self.form))
        text.append(">")
        return "".join(text)

    def response(self):
        """Return a copy of the current response.

        The returned object has the same interface as the object returned by
        :meth:`.open()`

        """
        pass

    def open_local_file(self, filename):
        pass

    def set_response(self, response):
        """Replace current response with (a copy of) response.

        response may be None.

        This is intended mostly for HTML-preprocessing.
        """
        pass

    def _set_response(self, response, close_current):
        # sanity check, necessary but far from sufficient
        pass

    def visit_response(self, response, request=None):
        """Visit the response, as if it had been :meth:`open()` ed.

        Unlike :meth:`set_response()`, this updates history rather than
        replacing the current response.
        """
        pass

    def _visit_request(self, request, update_history):
        pass

    def set_html(self, html, url="http://example.com/"):
        """Set the response to dummy with given HTML, and URL if given.

        Allows you to then parse that HTML, especially to extract forms
        information. If no URL was given then the default is "example.com".
        """
        pass

    def geturl(self):
        """Get URL of current document."""
        pass

    def reload(self):
        """Reload current document, and return response object."""
        pass

    def back(self, n=1):
        """Go back n steps in history, and return response object.

        n: go back this number of steps (default 1 step)

        """
        pass

    def clear_history(self):
        pass

    def set_cookie(self, cookie_string):
        """Set a cookie.

        Note that it is NOT necessary to call this method under ordinary
        circumstances: cookie handling is normally entirely automatic.  The
        intended use case is rather to simulate the setting of a cookie by
        client script in a web page (e.g. JavaScript).  In that case, use of
        this method is necessary because mechanize currently does not support
        JavaScript, VBScript, etc.

        The cookie is added in the same way as if it had arrived with the
        current response, as a result of the current request.  This means that,
        for example, if it is not appropriate to set the cookie based on the
        current request, no cookie will be set.

        The cookie will be returned automatically with subsequent responses
        made by the Browser instance whenever that's appropriate.

        cookie_string should be a valid value of the Set-Cookie header.

        For example:

        .. code-block:: python

            browser.set_cookie(
                "sid=abcdef; expires=Wednesday, 09-Nov-06 23:12:40 GMT")

        Currently, this method does not allow for adding RFC 2986 cookies.
        This limitation will be lifted if anybody requests it.

        See also :meth:`set_simple_cookie()` for an easier way to set cookies
        without needing to create a Set-Cookie header string.
        """
        pass

    def set_simple_cookie(self, name, value, domain, path='/'):
        '''
        Similar to :meth:`set_cookie()` except that instead of using a
        cookie string, you simply specify the `name`, `value`, `domain`
        and optionally the `path`.
        The created cookie will never expire. For example:

        .. code-block:: python

            browser.set_simple_cookie('some_key', 'some_value', '.example.com',
                                      path='/some-page')
        '''
        pass

    @property
    def cookiejar(self):
        ' Return the current cookiejar (:class:`mechanize.CookieJar`) or None '
        pass

    def set_header(self, header, value=None):
        '''
        Convenience method to set a header value in `self.addheaders`
        so that the header is sent out with all requests automatically.

        :param header: The header name, e.g. User-Agent
        :param value: The header value. If set to None the header is removed.
        '''
        pass

    def links(self, **kwds):
        """Return iterable over links (:class:`mechanize.Link` objects)."""
        pass

    def forms(self):
        """Return iterable over forms.

        The returned form objects implement the :class:`mechanize.HTMLForm`
        interface.

        """
        pass

    def global_form(self):
        """Return the global form object, or None if the factory implementation
        did not supply one.

        The "global" form object contains all controls that are not descendants
        of any FORM element.

        The returned form object implements the :class:`mechanize.HTMLForm`
        interface.

        This is a separate method since the global form is not regarded as part
        of the sequence of forms in the document -- mostly for
        backwards-compatibility.

        """
        pass

    def viewing_html(self):
        """Return whether the current response contains HTML data."""
        pass

    def encoding(self):
        pass

    def title(self):
        ' Return title, or None if there is no title element in the document. '
        pass

    def select_form(self, name=None, predicate=None, nr=None, **attrs):
        """Select an HTML form for input.

        This is a bit like giving a form the "input focus" in a browser.

        If a form is selected, the Browser object supports the HTMLForm
        interface, so you can call methods like :meth:`set_value()`,
        :meth:`set()`, and :meth:`click()`.

        Another way to select a form is to assign to the .form attribute.  The
        form assigned should be one of the objects returned by the
        :meth:`forms()` method.

        If no matching form is found,
        :class:`mechanize.FormNotFoundError` is raised.

        If `name` is specified, then the form must have the indicated name.

        If `predicate` is specified, then the form must match that function.
        The predicate function is passed the :class:`mechanize.HTMLForm` as its
        single argument, and should return a boolean value indicating whether
        the form matched.

        `nr`, if supplied, is the sequence number of the form (where 0 is the
        first).  Note that control 0 is the first form matching all the other
        arguments (if supplied); it is not necessarily the first control in the
        form.  The "global form" (consisting of all form controls not contained
        in any FORM element) is considered not to be part of this sequence and
        to have no name, so will not be matched unless both name and nr are
        None.

        You can also match on any HTML attribute of the `<form>` tag by passing
        in the attribute name and value as keyword arguments. To convert HTML
        attributes into syntactically valid python keyword arguments, the
        following simple rule is used. The python keyword argument name is
        converted to an HTML attribute name by: Replacing all underscores with
        hyphens and removing any trailing underscores. You can pass in strings,
        functions or regular expression objects as the values to match. For
        example:

        .. code-block:: python

            # Match form with the exact action specified
            br.select_form(action='http://foo.com/submit.php')
            # Match form with a class attribute that contains 'login'
            br.select_form(class_=lambda x: 'login' in x)
            # Match form with a data-form-type attribute that matches a regex
            br.select_form(data_form_type=re.compile(r'a|b'))

        """
        pass

    def click(self, *args, **kwds):
        """See :meth:`mechanize.HTMLForm.click()` for documentation."""
        pass

    def submit(self, *args, **kwds):
        """Submit current form.

        Arguments are as for :meth:`mechanize.HTMLForm.click()`.

        Return value is same as for :meth:`open()`.
        """
        pass

    def click_link(self, link=None, **kwds):
        """Find a link and return a Request object for it.

        Arguments are as for :meth:`find_link()`, except that a link may be
        supplied as the first argument.

        """
        pass

    def follow_link(self, link=None, **kwds):
        """Find a link and :meth:`open()` it.

        Arguments are as for :meth:`click_link()`.

        Return value is same as for :meth:`open()`.

        """
        pass

    def find_link(self,
                  text=None,
                  text_regex=None,
                  name=None,
                  name_regex=None,
                  url=None,
                  url_regex=None,
                  tag=None,
                  predicate=None,
                  nr=0):
        """Find a link in current page.

        Links are returned as :class:`mechanize.Link` objects. Examples:

        .. code-block:: python

            # Return third link that .search()-matches the regexp "python" (by
            # ".search()-matches", I mean that the regular expression method
            # .search() is used, rather than .match()).
            find_link(text_regex=re.compile("python"), nr=2)

            # Return first http link in the current page that points to
            # somewhere on python.org whose link text (after tags have been
            # removed) is exactly "monty python".
            find_link(text="monty python",
                    url_regex=re.compile("http.*python.org"))

            # Return first link with exactly three HTML attributes.
            find_link(predicate=lambda link: len(link.attrs) == 3)

        Links include anchors `<a>`, image maps `<area>`, and frames
        `<iframe>`.

        All arguments must be passed by keyword, not position.  Zero or more
        arguments may be supplied.  In order to find a link, all arguments
        supplied must match.

        If a matching link is not found, :class:`mechanize.LinkNotFoundError`
        is raised.

        :param text: link text between link tags: e.g. <a href="blah">this
            bit</a> with whitespace compressed.
        :param text_regex: link text between tag (as defined above) must match
            the regular expression object or regular expression string passed
            as this argument, if supplied
        :param name: as for text and text_regex, but matched
            against the name HTML attribute of the link tag
        :param url: as for text and text_regex, but matched against the
            URL of the link tag (note this matches against Link.url, which is a
            relative or absolute URL according to how it was written in the
            HTML)
        :param tag: element name of opening tag, e.g. "a"
        :param predicate: a function taking a Link object as its single
            argument, returning a boolean result, indicating whether the links
        :param nr: matches the nth link that matches all other
            criteria (default 0)

        """
        pass

    def __getattr__(self, name):
        # pass through _form.HTMLForm methods and attributes
        form = self.__dict__.get("form")
        if form is None:
            raise AttributeError(
                "%s instance has no attribute %s (perhaps you forgot to "
                ".select_form()?)" % (self.__class__, name))
        return getattr(form, name)

    def __getitem__(self, name):
        if self.form is None:
            raise BrowserStateError('No form selected')
        return self.form[name]

    def __setitem__(self, name, val):
        if self.form is None:
            raise BrowserStateError('No form selected')
        self.form[name] = val

    def _filter_links(self,
                      links,
                      text=None,
                      text_regex=None,
                      name=None,
                      name_regex=None,
                      url=None,
                      url_regex=None,
                      tag=None,
                      predicate=None,
                      nr=0):
        pass
