#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import absolute_import

import random
import re
import sys
import warnings
from io import BytesIO
from mimetypes import guess_type

from . import _request
from .polyglot import (as_unicode, is_py2, iteritems, unicode_type, urlencode,
                       urlparse, urlunparse)

if is_py2:
    from cStringIO import StringIO
else:
    class StringIO(BytesIO):

        def write(self, x):
            pass


class Missing:
    pass


class LocateError(ValueError):
    pass


class AmbiguityError(LocateError):
    pass


class ControlNotFoundError(LocateError):
    pass


class ItemNotFoundError(LocateError):
    pass


class ItemCountError(ValueError):
    pass


_compress_re = re.compile(r"\s+")


def deprecation(message, stack_offset=0):
    pass


def compress_whitespace(text):
    pass


def isstringlike(x):
    pass


def choose_boundary():
    """Return a string usable as a multipart boundary."""
    pass


# This cut-n-pasted MimeWriter from standard library is here so can add
# to HTTP headers rather than message body when appropriate.  It also uses
# \r\n in place of \n.  This is a bit nasty.
class MimeWriter:
    """Generic MIME writer.

    Methods:

    __init__()
    addheader()
    flushheaders()
    startbody()
    startmultipartbody()
    nextpart()
    lastpart()

    A MIME writer is much more primitive than a MIME parser.  It
    doesn't seek around on the output file, and it doesn't use large
    amounts of buffer space, so you have to write the parts in the
    order they should occur on the output file.  It does buffer the
    headers you add, allowing you to rearrange their order.

    General usage is:

    .. code-block:: python

        f = <open the output file>
        w = MimeWriter(f)
        ...call w.addheader(key, value) 0 or more times...

    followed by either:

    .. code-block:: python

        f = w.startbody(content_type)
        ...call f.write(data) for body data...

    or:

    .. code-block:: python

        w.startmultipartbody(subtype)
        for each part:
            subwriter = w.nextpart()
            ...use the subwriter's methods to create the subpart...
        w.lastpart()

    The subwriter is another MimeWriter instance, and should be
    treated in the same way as the toplevel MimeWriter.  This way,
    writing recursive body parts is easy.

    Warning: don't forget to call lastpart()!

    XXX There should be more state so calls made in the wrong order
    are detected.

    Some special cases:

    - startbody() just returns the file passed to the constructor;
      but don't use this knowledge, as it may be changed.

    - startmultipartbody() actually returns a file as well;
      this can be used to write the initial 'if you can read this your
      mailer is not MIME-aware' message.

    - If you call flushheaders(), the headers accumulated so far are
      written out (and forgotten); this is useful if you don't need a
      body part at all, e.g. for a subpart of type message/rfc822
      that's (mis)used to store some header-like information.

    - Passing a keyword argument 'prefix=<flag>' to addheader(),
      start*body() affects where the header is inserted; 0 means
      append at the end, 1 means insert at the start; default is
      append for addheader(), but insert for start*body(), which use
      it to determine where the Content-type header goes.

    """

    def __init__(self, fp, http_hdrs=None):
        self._http_hdrs = http_hdrs
        self._fp = fp
        self._headers = []
        self._boundary = []
        self._first_part = True

    def addheader(self, key, value, prefix=0, add_to_http_hdrs=0):
        """
        prefix is ignored if add_to_http_hdrs is true.
        """
        pass

    def flushheaders(self):
        pass

    def startbody(self,
                  ctype=None,
                  plist=[],
                  prefix=1,
                  add_to_http_hdrs=0,
                  content_type=1):
        """
        prefix is ignored if add_to_http_hdrs is true.
        """
        pass

    def startmultipartbody(self,
                           subtype,
                           boundary=None,
                           plist=[],
                           prefix=1,
                           add_to_http_hdrs=0,
                           content_type=1):
        pass

    def nextpart(self):
        pass

    def lastpart(self):
        pass


class Label:
    def __init__(self, text, for_id=None):
        self.id = for_id
        self.text = compress_whitespace(text or '')

    def __repr__(self):
        return "<Label(id=%r, text=%r)>" % (self.id, self.text)

    __str__ = __repr__


def _get_label(attrs):
    pass


class Control:
    """An HTML form control.

    An HTMLForm contains a sequence of Controls.  The Controls in an HTMLForm
    are accessed using the HTMLForm.find_control method or the
    HTMLForm.controls attribute.

    Control instances are usually constructed using the ParseFile /
    ParseResponse functions.  If you use those functions, you can ignore the
    rest of this paragraph.  A Control is only properly initialised after the
    fixup method has been called.  In fact, this is only strictly necessary for
    ListControl instances.  This is necessary because ListControls are built up
    from ListControls each containing only a single item, and their initial
    value(s) can only be known after the sequence is complete.

    The types and values that are acceptable for assignment to the value
    attribute are defined by subclasses.

    If the disabled attribute is true, this represents the state typically
    represented by browsers by 'greying out' a control.  If the disabled
    attribute is true, the Control will raise AttributeError if an attempt is
    made to change its value.  In addition, the control will not be considered
    'successful' as defined by the W3C HTML 4 standard -- ie. it will
    contribute no data to the return value of the HTMLForm.click* methods.  To
    enable a control, set the disabled attribute to a false value.

    If the readonly attribute is true, the Control will raise AttributeError if
    an attempt is made to change its value.  To make a control writable, set
    the readonly attribute to a false value.

    All controls have the disabled and readonly attributes, not only those that
    may have the HTML attributes of the same names.

    On assignment to the value attribute, the following exceptions are raised:
    TypeError, AttributeError (if the value attribute should not be assigned
    to, because the control is disabled, for example) and ValueError.

    If the name or value attributes are None, or the value is an empty list, or
    if the control is disabled, the control is not successful.

    Public attributes:

    :ivar str type: string describing type of control (see the keys of the
        HTMLForm.type2class dictionary for the allowable values) (readonly)
    :ivar str name: name of control (readonly)
    :ivar value: current value of control (subclasses may allow a single value,
        a sequence of values, or either)
    :ivar bool disabled: disabled state
    :ivar bool readonly: readonly state
    :ivar str id: value of id HTML attribute

    """

    def __init__(self, type, name, attrs, index=None):
        """
        type: string describing type of control (see the keys of the
         HTMLForm.type2class dictionary for the allowable values)
        name: control name
        attrs: HTML attributes of control's HTML element

        """
        pass

    def add_to_form(self, form):
        pass

    def fixup(self):
        pass

    def is_of_kind(self, kind):
        pass

    def clear(self):
        pass

    def __getattr__(self, name):
        raise NotImplementedError()

    def __setattr__(self, name, value):
        raise NotImplementedError()

    def pairs(self):
        """Return list of (key, value) pairs suitable for passing to urlencode.
        """
        pass

    def _totally_ordered_pairs(self):
        """Return list of (key, value, index) tuples.

        Like pairs, but allows preserving correct ordering even where several
        controls are involved.

        """
        pass

    def _write_mime_data(self, mw, name, value):
        """Write data for a subitem of this control to a MimeWriter."""
        pass

    def __str__(self):
        raise NotImplementedError()

    def get_labels(self):
        """Return all labels (Label instances) for this control.

        If the control was surrounded by a <label> tag, that will be the first
        label; all other labels, connected by 'for' and 'id', are in the order
        that appear in the HTML.

        """
        pass


# ---------------------------------------------------
class ScalarControl(Control):
    """Control whose value is not restricted to one of a prescribed set.

    Some ScalarControls don't accept any value attribute.  Otherwise, takes a
    single value, which must be string-like.

    Additional read-only public attribute:

    :ivar dict attrs: dictionary mapping the names of original HTML attributes
        of the control to their values

    """

    def __init__(self, type, name, attrs, index=None):
        self._index = index
        self._label = _get_label(attrs)
        self.__dict__["type"] = type.lower()
        self.__dict__["name"] = name
        self._value = attrs.get("value")
        self.disabled = 'disabled' in attrs
        self.readonly = 'readonly' in attrs
        self.id = attrs.get("id")

        self.attrs = dict(attrs)

        self._clicked = False

        self._urlparse = urlparse
        self._urlunparse = urlunparse

    def __getattr__(self, name):
        if name == "value":
            return self.__dict__["_value"]
        else:
            raise AttributeError("%s instance has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name == "value":
            if not isstringlike(value):
                raise TypeError("must assign a string")
            elif self.readonly:
                raise AttributeError("control '%s' is readonly" % self.name)
            elif self.disabled:
                raise AttributeError("control '%s' is disabled" % self.name)
            self.__dict__["_value"] = value
        elif name in ("name", "type"):
            raise AttributeError("%s attribute is readonly" % name)
        else:
            self.__dict__[name] = value

    def _totally_ordered_pairs(self):
        pass

    def clear(self):
        pass

    def __str__(self):
        name = self.name
        value = self.value
        if name is None:
            name = "<None>"
        if value is None:
            value = "<None>"

        infos = []
        if self.disabled:
            infos.append("disabled")
        if self.readonly:
            infos.append("readonly")
        info = ", ".join(infos)
        if info:
            info = " (%s)" % info

        return "<%s(%s=%s)%s>" % (self.__class__.__name__, name, value, info)


# ---------------------------------------------------
class TextControl(ScalarControl):
    """Textual input control.

    Covers HTML elements: INPUT/TEXT, INPUT/PASSWORD, INPUT/HIDDEN, TEXTAREA

    """

    def __init__(self, type, name, attrs, index=None):
        pass

    def is_of_kind(self, kind):
        pass


# ---------------------------------------------------
class FileControl(ScalarControl):
    """File upload with INPUT TYPE=FILE.

    The value attribute of a FileControl is always None.  Use add_file instead.

    Additional public method: :meth:`add_file`

    """

    def __init__(self, type, name, attrs, index=None):
        pass

    def is_of_kind(self, kind):
        pass

    def clear(self):
        pass

    def __setattr__(self, name, value):
        if name in ("value", "name", "type"):
            raise AttributeError("%s attribute is readonly" % name)
        else:
            self.__dict__[name] = value

    def add_file(self, file_object, content_type=None, filename=None):
        ''' Add data from the specified file to be uploaded. content_type and
        filename are sent in the HTTP headers if specified. '''
        pass

    def _totally_ordered_pairs(self):
        # XXX should it be successful even if unnamed?
        pass

    # If enctype is application/x-www-form-urlencoded and there's a FILE
    # control present, what should be sent?  Strictly, it should be 'name=data'
    # (see HTML 4.01 spec., section 17.13.2), but code sends "name=" ATM.  What
    # about multiple file upload?
    def _write_mime_data(self, mw, _name, _value):
        # called by HTMLForm
        # assert _name == self.name and _value == ''
        pass

    def __str__(self):
        name = self.name
        if name is None:
            name = "<None>"

        if not self._upload_data:
            value = "<No files added>"
        else:
            value = []
            for file, ctype, filename in self._upload_data:
                if filename is None:
                    value.append("<Unnamed file>")
                else:
                    value.append(filename)
            value = ", ".join(value)

        info = []
        if self.disabled:
            info.append("disabled")
        if self.readonly:
            info.append("readonly")
        info = ", ".join(info)
        if info:
            info = " (%s)" % info

        return "<%s(%s=%s)%s>" % (self.__class__.__name__, name, value, info)


# ---------------------------------------------------
# ---------------------------------------------------
class IgnoreControl(ScalarControl):
    """Control that we're not interested in.

    Covers html elements: INPUT/RESET, BUTTON/RESET, INPUT/BUTTON,
    BUTTON/BUTTON

    These controls are always unsuccessful, in the terminology of HTML 4 (ie.
    they never require any information to be returned to the server).

    BUTTON/BUTTON is used to generate events for script embedded in HTML.

    The value attribute of IgnoreControl is always None.

    """

    def __init__(self, type, name, attrs, index=None):
        pass

    def is_of_kind(self, kind):
        pass

    def __setattr__(self, name, value):
        if name == "value":
            raise AttributeError("control '%s' is ignored, hence read-only" %
                                 self.name)
        elif name in ("name", "type"):
            raise AttributeError("%s attribute is readonly" % name)
        else:
            self.__dict__[name] = value


# ---------------------------------------------------
# ListControls

# helpers and subsidiary classes


class Item:
    def __init__(self, control, attrs, index=None):
        pass

    def get_labels(self):
        """Return all labels (Label instances) for this item.

        For items that represent radio buttons or checkboxes, if the item was
        surrounded by a <label> tag, that will be the first label; all other
        labels, connected by 'for' and 'id', are in the order that appear in
        the HTML.

        For items that represent select options, if the option had a label
        attribute, that will be the first label.  If the option has contents
        (text within the option tags) and it is not the same as the label
        attribute (if any), that will be a label.  There is nothing in the
        spec to my knowledge that makes an option with an id unable to be the
        target of a label's for attribute, so those are included, if any, for
        the sake of consistency and completeness.

        """
        pass

    def __getattr__(self, name):
        if name == "selected":
            return self._selected
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == "selected":
            self._control._set_selected_state(self, value)
        elif name == "disabled":
            self.__dict__["disabled"] = bool(value)
        else:
            raise AttributeError(name)

    def __str__(self):
        res = self.name
        if self.selected:
            res = "*" + res
        if self.disabled:
            res = "(%s)" % res
        return res

    def __repr__(self):
        # XXX appending the attrs without distinguishing them from name and id
        # is silly
        attrs = [("name", self.name), ("id", self.id)] + list(
                iteritems(self.attrs))
        return "<%s %s>" % (self.__class__.__name__,
                            " ".join(["%s=%r" % (k, v) for k, v in attrs]))


def disambiguate(items, nr, **kwds):
    pass


class ListControl(Control):
    """Control representing a sequence of items.

    The value attribute of a ListControl represents the successful list items
    in the control.  The successful list items are those that are selected and
    not disabled.

    ListControl implements both list controls that take a length-1 value
    (single-selection) and those that take length >1 values
    (multiple-selection).

    ListControls accept sequence values only.  Some controls only accept
    sequences of length 0 or 1 (RADIO, and single-selection SELECT).
    In those cases, ItemCountError is raised if len(sequence) > 1.  CHECKBOXes
    and multiple-selection SELECTs (those having the "multiple" HTML attribute)
    accept sequences of any length.

    Note the following mistake:

    .. code-block:: python

        control.value = some_value
        assert control.value == some_value    # not necessarily true

    The reason for this is that the value attribute always gives the list items
    in the order they were listed in the HTML.

    ListControl items can also be referred to by their labels instead of names.
    Use the label argument to .get(), and the .set_value_by_label(),
    .get_value_by_label() methods.

    Note that, rather confusingly, though SELECT controls are represented in
    HTML by SELECT elements (which contain OPTION elements, representing
    individual list items), CHECKBOXes and RADIOs are not represented by *any*
    element.  Instead, those controls are represented by a collection of INPUT
    elements.  For example, this is a SELECT control, named "control1"::

        <select name="control1">
        <option>foo</option>
        <option value="1">bar</option>
        </select>

    and this is a CHECKBOX control, named "control2"::

        <input type="checkbox" name="control2" value="foo" id="cbe1">
        <input type="checkbox" name="control2" value="bar" id="cbe2">

    The id attribute of a CHECKBOX or RADIO ListControl is always that of its
    first element (for example, "cbe1" above).


    Additional read-only public attribute: multiple.

    """

    # ListControls are built up by the parser from their component items by
    # creating one ListControl per item, consolidating them into a single
    # master ListControl held by the HTMLForm:

    # -User calls form.new_control(...)
    # -Form creates Control, and calls control.add_to_form(self).
    # -Control looks for a Control with the same name and type in the form,
    #  and if it finds one, merges itself with that control by calling
    #  control.merge_control(self).  The first Control added to the form, of
    #  a particular name and type, is the only one that survives in the
    #  form.
    # -Form calls control.fixup for all its controls.  ListControls in the
    #  form know they can now safely pick their default values.

    # To create a ListControl without an HTMLForm, use:

    # control.merge_control(new_control)

    # (actually, it's much easier just to use ParseFile)

    _label = None

    def __init__(self,
                 type,
                 name,
                 attrs={},
                 select_default=False,
                 called_as_base_class=False,
                 index=None):
        """
        select_default: for RADIO and multiple-selection SELECT controls, pick
         the first item as the default if no 'selected' HTML attribute is
         present

        """
        pass

    def clear(self):
        pass

    def is_of_kind(self, kind):
        pass

    def get_items(self, name=None, label=None, id=None,
                  exclude_disabled=False):
        """Return matching items by name or label.

        For argument docs, see the docstring for .get()

        """
        pass

    def get(self,
            name=None,
            label=None,
            id=None,
            nr=None,
            exclude_disabled=False):
        """Return item by name or label, disambiguating if necessary with nr.

        All arguments must be passed by name, with the exception of 'name',
        which may be used as a positional argument.

        If name is specified, then the item must have the indicated name.

        If label is specified, then the item must have a label whose
        whitespace-compressed, stripped, text substring-matches the indicated
        label string (e.g. label="please choose" will match
        "  Do  please  choose an item ").

        If id is specified, then the item must have the indicated id.

        nr is an optional 0-based index of the items matching the query.

        If nr is the default None value and more than item is found, raises
        AmbiguityError.

        If no item is found, or if items are found but nr is specified and not
        found, raises ItemNotFoundError.

        Optionally excludes disabled items.

        """
        pass

    def _get(self, name, by_label=False, nr=None, exclude_disabled=False):
        # strictly for use by deprecated methods
        pass

    def toggle(self, name, by_label=False, nr=None):
        """Deprecated: given a name or label and optional disambiguating index
        nr, toggle the matching item's selection.

        Selecting items follows the behavior described in the docstring of the
        'get' method.

        if the item is disabled, or this control is disabled or readonly,
        raise AttributeError.

        """
        pass

    def set(self, selected, name, by_label=False, nr=None):
        """Deprecated: given a name or label and optional disambiguating index
        nr, set the matching item's selection to the bool value of selected.

        Selecting items follows the behavior described in the docstring of the
        'get' method.

        if the item is disabled, or this control is disabled or readonly,
        raise AttributeError.

        """
        pass

    def _set_selected_state(self, item, action):
        # action:
        # bool False: off
        # bool True: on
        pass

    def toggle_single(self, by_label=None):
        """Deprecated: toggle the selection of the single item in this control.

        Raises ItemCountError if the control does not contain only one item.

        by_label argument is ignored, and included only for backwards
        compatibility.

        """
        pass

    def set_single(self, selected, by_label=None):
        """Deprecated: set the selection of the single item in this control.

        Raises ItemCountError if the control does not contain only one item.

        by_label argument is ignored, and included only for backwards
        compatibility.

        """
        pass

    def get_item_disabled(self, name, by_label=False, nr=None):
        """Get disabled state of named list item in a ListControl."""
        pass

    def set_item_disabled(self, disabled, name, by_label=False, nr=None):
        """Set disabled state of named list item in a ListControl.

        :arg disabled: boolean disabled state

        """
        pass

    def set_all_items_disabled(self, disabled):
        """Set disabled state of all list items in a ListControl.

        :arg disabled: boolean disabled state

        """
        pass

    def get_item_attrs(self, name, by_label=False, nr=None):
        """Return dictionary of HTML attributes for a single ListControl item.

        The HTML element types that describe list items are: OPTION for SELECT
        controls, INPUT for the rest.  These elements have HTML attributes that
        you may occasionally want to know about -- for example, the "alt" HTML
        attribute gives a text string describing the item (graphical browsers
        usually display this as a tooltip).

        The returned dictionary maps HTML attribute names to values.  The names
        and values are taken from the original HTML.

        """
        pass

    def close_control(self):
        pass

    def add_to_form(self, form):
        pass

    def merge_control(self, control):
        pass

    def fixup(self):
        """
        ListControls are built up from component list items (which are also
        ListControls) during parsing.  This method should be called after all
        items have been added.  See :class:`mechanize.ListControl` for the
        reason this is required.

        """
        pass

    def __getattr__(self, name):
        if name == "value":
            if self.name is None:
                return []
            return [
                o.name for o in self.items if o.selected and (not o.disabled)
            ]
        else:
            raise AttributeError("%s instance has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name == "value":
            if self.disabled:
                raise AttributeError("control '%s' is disabled" % self.name)
            if self.readonly:
                raise AttributeError("control '%s' is readonly" % self.name)
            self._set_value(value)
        elif name in ("name", "type", "multiple"):
            raise AttributeError("%s attribute is readonly" % name)
        else:
            self.__dict__[name] = value

    def _set_value(self, value):
        pass

    def _get_items(self, name, target=1):
        pass

    def _single_set_value(self, value):
        pass

    def _multiple_set_value(self, value):
        pass

    def set_value_by_label(self, value):
        """Set the value of control by item labels.

        value is expected to be an iterable of strings that are substrings of
        the item labels that should be selected.  Before substring matching is
        performed, the original label text is whitespace-compressed
        (consecutive whitespace characters are converted to a single space
        character) and leading and trailing whitespace is stripped. Ambiguous
        labels: it will not complain as long as all ambiguous labels share the
        same item name (e.g. OPTION value).

        """
        pass

    def get_value_by_label(self):
        """Return the value of the control as given by normalized labels."""
        pass

    def possible_items(self, by_label=False):
        """Deprecated: return the names or labels of all possible items.

        Includes disabled items, which may be misleading for some use cases.

        """
        pass

    def _totally_ordered_pairs(self):
        pass

    def __str__(self):
        name = self.name
        if name is None:
            name = "<None>"

        display = [str(o) for o in self.items]

        infos = []
        if self.disabled:
            infos.append("disabled")
        if self.readonly:
            infos.append("readonly")
        info = ", ".join(infos)
        if info:
            info = " (%s)" % info

        return "<%s(%s=[%s])%s>" % (self.__class__.__name__, name,
                                    ", ".join(display), info)


class RadioControl(ListControl):
    """
    Covers:

    INPUT/RADIO

    """

    def __init__(self, type, name, attrs, select_default=False, index=None):
        pass

    def fixup(self):
        pass

    def get_labels(self):
        pass


class CheckboxControl(ListControl):
    """
    Covers:

    INPUT/CHECKBOX

    """

    def __init__(self, type, name, attrs, select_default=False, index=None):
        pass

    def get_labels(self):
        pass


class SelectControl(ListControl):
    """
    Covers:

    SELECT (and OPTION)


    OPTION 'values', in HTML parlance, are Item 'names' in mechanize parlance.

    SELECT control values and labels are subject to some messy defaulting
    rules.  For example, if the HTML representation of the control is::

        <SELECT name=year>
            <OPTION value=0 label="2002">current year</OPTION>
            <OPTION value=1>2001</OPTION>
            <OPTION>2000</OPTION>
        </SELECT>

    The items, in order, have labels "2002", "2001" and "2000", whereas their
    names (the OPTION values) are "0", "1" and "2000" respectively.  Note that
    the value of the last OPTION in this example defaults to its contents, as
    specified by RFC 1866, as do the labels of the second and third OPTIONs.

    The OPTION labels are sometimes more meaningful than the OPTION values,
    which can make for more maintainable code.

    Additional read-only public attribute: attrs

    The attrs attribute is a dictionary of the original HTML attributes of the
    SELECT element.  Other ListControls do not have this attribute, because in
    other cases the control as a whole does not correspond to any single HTML
    element.  control.get(...).attrs may be used as usual to get at the HTML
    attributes of the HTML elements corresponding to individual list items (for
    SELECT controls, these are OPTION elements).

    Another special case is that the Item.attrs dictionaries have a special key
    "contents" which does not correspond to any real HTML attribute, but rather
    contains the contents of the OPTION element::

        <OPTION>this bit</OPTION>

    """

    # HTML attributes here are treated slightly differently from other list
    # controls:
    # -The SELECT HTML attributes dictionary is stuffed into the OPTION
    #  HTML attributes dictionary under the "__select" key.
    # -The content of each OPTION element is stored under the special
    #  "contents" key of the dictionary.
    # After all this, the dictionary is passed to the SelectControl constructor
    # as the attrs argument, as usual.  However:
    # -The first SelectControl constructed when building up a SELECT control
    #  has a constructor attrs argument containing only the __select key -- so
    #  this SelectControl represents an empty SELECT control.
    # -Subsequent SelectControls have both OPTION HTML-attribute in attrs and
    #  the __select dictionary containing the SELECT HTML-attributes.

    def __init__(self, type, name, attrs, select_default=False, index=None):
        # fish out the SELECT HTML attributes from the OPTION HTML attributes
        # dictionary
        pass

    def fixup(self):
        pass


# ---------------------------------------------------
class SubmitControl(ScalarControl):
    """
    Covers:

    INPUT/SUBMIT
    BUTTON/SUBMIT

    """

    def __init__(self, type, name, attrs, index=None):
        pass

    def get_labels(self):
        pass

    def is_of_kind(self, kind):
        pass

    def _click(self, form, coord, return_type, request_class=_request.Request):
        pass

    def _totally_ordered_pairs(self):
        pass


# ---------------------------------------------------
class ImageControl(SubmitControl):
    """
    Covers:

    INPUT/IMAGE

    Coordinates are specified using one of the HTMLForm.click* methods.

    """

    def __init__(self, type, name, attrs, index=None):
        pass

    def _totally_ordered_pairs(self):
        pass

    get_labels = ScalarControl.get_labels


# aliases, just to make str(control) and str(form) clearer
class PasswordControl(TextControl):
    pass


class HiddenControl(TextControl):
    pass


class TextareaControl(TextControl):
    pass


class SubmitButtonControl(SubmitControl):
    pass


def is_listcontrol(control):
    pass


class HTMLForm:
    """
    Represents a single HTML <form> ... </form> element.

    A form consists of a sequence of controls that usually have names, and
    which can take on various values.  The values of the various types of
    controls represent variously: text, zero-or-one-of-many or many-of-many
    choices, and files to be uploaded.  Some controls can be clicked on to
    submit the form, and clickable controls' values sometimes include the
    coordinates of the click.

    Forms can be filled in with data to be returned to the server, and then
    submitted, using the click method to generate a request object suitable for
    passing to :func:`mechanize.urlopen` (or the click_request_data or
    click_pairs methods for integration with third-party code).

    Usually, HTMLForm instances are not created directly.  Instead, they are
    automatically created when visting a page with a mechanize Browser.  If you
    do construct HTMLForm objects yourself, however, note that an HTMLForm
    instance is only properly initialised after the fixup method has been
    called.  See :class:`mechanize.ListControl` for the reason this is
    required.

    Indexing a form (form["control_name"]) returns the named Control's value
    attribute.  Assignment to a form index (form["control_name"] = something)
    is equivalent to assignment to the named Control's value attribute.  If you
    need to be more specific than just supplying the control's name, use the
    set_value and get_value methods.

    ListControl values are lists of item names (specifically, the names of the
    items that are selected and not disabled, and hence are "successful" -- ie.
    cause data to be returned to the server).  The list item's name is the
    value of the corresponding HTML element's"value" attribute.

    Example::

      <INPUT type="CHECKBOX" name="cheeses" value="leicester"></INPUT>
      <INPUT type="CHECKBOX" name="cheeses" value="cheddar"></INPUT>

    defines a CHECKBOX control with name "cheeses" which has two items, named
    "leicester" and "cheddar".

    Another example::

      <SELECT name="more_cheeses">
        <OPTION>1</OPTION>
        <OPTION value="2" label="CHEDDAR">cheddar</OPTION>
      </SELECT>

    defines a SELECT control with name "more_cheeses" which has two items,
    named "1" and "2" (because the OPTION element's value HTML attribute
    defaults to the element contents -- see :class:`mechanize.SelectControl`
    for more on these defaulting rules).

    To select, deselect or otherwise manipulate individual list items, use the
    :meth:`mechanize.HTMLForm.find_control()` and
    :meth:`mechanize.ListControl.get()` methods.  To set the whole value, do as
    for any other control: use indexing or the `set_value/get_value` methods.

    Example:

    .. code-block:: python

        # select *only* the item named "cheddar"
        form["cheeses"] = ["cheddar"]
        # select "cheddar", leave other items unaffected
        form.find_control("cheeses").get("cheddar").selected = True

    Some controls (RADIO and SELECT without the multiple attribute) can only
    have zero or one items selected at a time.  Some controls (CHECKBOX and
    SELECT with the multiple attribute) can have multiple items selected at a
    time.  To set the whole value of a ListControl, assign a sequence to a form
    index:

    .. code-block:: python

        form["cheeses"] = ["cheddar", "leicester"]

    If the ListControl is not multiple-selection, the assigned list must be of
    length one.

    To check if a control has an item, if an item is selected, or if an item is
    successful (selected and not disabled), respectively:

    .. code-block:: python

        "cheddar" in [item.name for item in form.find_control("cheeses").items]
        "cheddar" in [item.name for item in form.find_control("cheeses").items
                        and item.selected]
        "cheddar" in form["cheeses"]
        # or
        "cheddar" in form.get_value("cheeses")

    Note that some list items may be disabled (see below).

    Note the following mistake:

    .. code-block:: python

        form[control_name] = control_value
        assert form[control_name] == control_value  # not necessarily true

    The reason for this is that form[control_name] always gives the list items
    in the order they were listed in the HTML.

    List items (hence list values, too) can be referred to in terms of list
    item labels rather than list item names using the appropriate label
    arguments.  Note that each item may have several labels.

    The question of default values of OPTION contents, labels and values is
    somewhat complicated: see :class:`mechanize.SelectControl` and
    :meth:`mechanize.ListControl.get_item_attrs()` if you think you need to
    know.

    Controls can be disabled or readonly.  In either case, the control's value
    cannot be changed until you clear those flags (see example below).
    Disabled is the state typically represented by browsers by 'greying out' a
    control.  Disabled controls are not 'successful' -- they don't cause data
    to get returned to the server.  Readonly controls usually appear in
    browsers as read-only text boxes.  Readonly controls are successful.  List
    items can also be disabled.  Attempts to select or deselect disabled items
    fail with AttributeError.

    If a lot of controls are readonly, it can be useful to do this:

    .. code-block:: python

        form.set_all_readonly(False)

    To clear a control's value attribute, so that it is not successful (until a
    value is subsequently set):

    .. code-block:: python

        form.clear("cheeses")

    More examples:

    .. code-block:: python

        control = form.find_control("cheeses")
        control.disabled = False
        control.readonly = False
        control.get("gruyere").disabled = True
        control.items[0].selected = True

    See the various Control classes for further documentation.  Many methods
    take name, type, kind, id, label and nr arguments to specify the control to
    be operated on: see :meth:`mechanize.HTMLForm.find_control()`.

    ControlNotFoundError (subclass of ValueError) is raised if the specified
    control can't be found.  This includes occasions where a non-ListControl
    is found, but the method (set, for example) requires a ListControl.
    ItemNotFoundError (subclass of ValueError) is raised if a list item can't
    be found.  ItemCountError (subclass of ValueError) is raised if an attempt
    is made to select more than one item and the control doesn't allow that, or
    set/get_single are called and the control contains more than one item.
    AttributeError is raised if a control or item is readonly or disabled and
    an attempt is made to alter its value.

    Security note: Remember that any passwords you store in HTMLForm instances
    will be saved to disk in the clear if you pickle them (directly or
    indirectly).  The simplest solution to this is to avoid pickling HTMLForm
    objects.  You could also pickle before filling in any password, or just set
    the password to "" before pickling.


    Public attributes:

    :ivar action: full (absolute URI) form action
    :ivar method: "GET" or "POST"
    :ivar enctype: form transfer encoding MIME type
    :ivar name: name of form (None if no name was specified)
    :ivar attrs: dictionary mapping original HTML form attributes to their
        values
    :ivar controls: list of Control instances; do not alter this list
        (instead, call form.new_control to make a Control and add it to the
        form, or control.add_to_form if you already have a Control instance)



    Methods for form filling:

    Most of the these methods have very similar arguments.  See
    :meth:`mechanize.HTMLForm.find_control()` for details of the name, type,
    kind, label and nr arguments.

    .. code-block:: python

        def find_control(self,
                        name=None, type=None, kind=None, id=None,
                        predicate=None, nr=None, label=None)

        get_value(name=None, type=None, kind=None, id=None, nr=None,
                by_label=False,  # by_label is deprecated
                label=None)
        set_value(value,
                name=None, type=None, kind=None, id=None, nr=None,
                by_label=False,  # by_label is deprecated
                label=None)

        clear_all()
        clear(name=None, type=None, kind=None, id=None, nr=None, label=None)

        set_all_readonly(readonly)


    Method applying only to FileControls:

    .. code-block:: python

        add_file(file_object,
             content_type="application/octet-stream", filename=None,
             name=None, id=None, nr=None, label=None)


    Methods applying only to clickable controls:

    .. code-block:: python

        click(name=None, type=None, id=None, nr=0, coord=(1,1), label=None)
        click_request_data(name=None, type=None, id=None, nr=0, coord=(1,1),
                        label=None)
        click_pairs(name=None, type=None, id=None, nr=0, coord=(1,1),
                        label=None)

    """

    type2class = {
        "text": TextControl,
        "password": PasswordControl,
        "hidden": HiddenControl,
        "textarea": TextareaControl,
        "file": FileControl,
        "button": IgnoreControl,
        "buttonbutton": IgnoreControl,
        "reset": IgnoreControl,
        "resetbutton": IgnoreControl,
        "submit": SubmitControl,
        "submitbutton": SubmitButtonControl,
        "image": ImageControl,
        "radio": RadioControl,
        "checkbox": CheckboxControl,
        "select": SelectControl,
    }

    # ---------------------------------------------------
    # Initialisation.  Use ParseResponse / ParseFile instead.

    def __init__(self,
                 action,
                 method="GET",
                 enctype="application/x-www-form-urlencoded",
                 name=None,
                 attrs=None,
                 request_class=_request.Request,
                 forms=None,
                 labels=None,
                 id_to_labels=None,
                 encoding=None):
        """
        In the usual case, use ParseResponse (or ParseFile) to create new
        HTMLForm objects.

        action: full (absolute URI) form action
        method: "GET" or "POST"
        enctype: form transfer encoding MIME type
        name: name of form
        attrs: dictionary mapping original HTML form attributes to their values

        """
        pass

    def new_control(self,
                    type,
                    name,
                    attrs,
                    ignore_unknown=False,
                    select_default=False,
                    index=None):
        """Adds a new control to the form.

        This is usually called by mechanize.  Don't call it
        yourself unless you're building your own Control instances.

        Note that controls representing lists of items are built up from
        controls holding only a single list item.  See
        :class:`mechanize.ListControl` for further information.

        :arg type: type of control (see :class:`mechanize.Control` for a list)
        :arg attrs: HTML attributes of control
        :arg ignore_unknown: if true, use a dummy Control instance for controls
            of unknown type; otherwise, use a TextControl
        :arg select_default: for RADIO and multiple-selection SELECT controls,
            pick the first item as the default if no 'selected' HTML attribute
            is present (this defaulting happens when the HTMLForm.fixup method
            is called)
        :arg index: index of corresponding element in HTML (see
            MoreFormTests.test_interspersed_controls for motivation)

        """
        pass

    def fixup(self):
        """Normalise form after all controls have been added.

        This is usually called by ParseFile and ParseResponse.  Don't call it
        youself unless you're building your own Control instances.

        This method should only be called once, after all controls have been
        added to the form.

        """
        pass

# ---------------------------------------------------

    def __str__(self):
        header = "%s%s %s %s" % ((self.name and self.name + " " or ""),
                                 self.method, self.action, self.enctype)
        rep = [header]
        for control in self.controls:
            rep.append("  %s" % str(control))
        return "<%s>" % "\n".join(rep)

# ---------------------------------------------------
# Form-filling methods.

    def __getitem__(self, name):
        return self.find_control(name).value

    def __contains__(self, name):
        return bool(self.find_control(name))

    def __setitem__(self, name, value):
        control = self.find_control(name)
        try:
            control.value = value
        except AttributeError as e:
            raise ValueError(str(e))

    def get_value(
            self,
            name=None,
            type=None,
            kind=None,
            id=None,
            nr=None,
            by_label=False,  # by_label is deprecated
            label=None):
        """Return value of control.

        If only name and value arguments are supplied, equivalent to

        .. code-block:: python

            form[name]

        """
        pass

    def set_value(
            self,
            value,
            name=None,
            type=None,
            kind=None,
            id=None,
            nr=None,
            by_label=False,  # by_label is deprecated
            label=None):
        """Set value of control.

        If only name and value arguments are supplied, equivalent to

        .. code-block:: python

            form[name] = value

        """
        pass

    def get_value_by_label(self,
                           name=None,
                           type=None,
                           kind=None,
                           id=None,
                           label=None,
                           nr=None):
        """

        All arguments should be passed by name.

        """
        pass

    def set_value_by_label(self,
                           value,
                           name=None,
                           type=None,
                           kind=None,
                           id=None,
                           label=None,
                           nr=None):
        """

        All arguments should be passed by name.

        """
        pass

    def set_all_readonly(self, readonly):
        pass

    def clear_all(self):
        """Clear the value attributes of all controls in the form.

        See :meth:`mechanize.HTMLForm.clear()`

        """
        pass

    def clear(self,
              name=None,
              type=None,
              kind=None,
              id=None,
              nr=None,
              label=None):
        """Clear the value attribute of a control.

        As a result, the affected control will not be successful until a value
        is subsequently set.  AttributeError is raised on readonly controls.

        """
        pass

# ---------------------------------------------------
# Form-filling methods applying only to ListControls.

    def possible_items(
            self,  # deprecated
            name=None,
            type=None,
            kind=None,
            id=None,
            nr=None,
            by_label=False,
            label=None):
        """Return a list of all values that the specified control can take."""
        pass

    def set(
            self,
            selected,
            item_name,  # deprecated
            name=None,
            type=None,
            kind=None,
            id=None,
            nr=None,
            by_label=False,
            label=None):
        """Select / deselect named list item.

        :arg selected: boolean selected state

        """
        pass

    def toggle(
            self,
            item_name,  # deprecated
            name=None,
            type=None,
            kind=None,
            id=None,
            nr=None,
            by_label=False,
            label=None):
        """Toggle selected state of named list item."""
        pass

    def set_single(
            self,
            selected,  # deprecated
            name=None,
            type=None,
            kind=None,
            id=None,
            nr=None,
            by_label=None,
            label=None):
        """Select / deselect list item in a control having only one item.

        If the control has multiple list items, ItemCountError is raised.

        This is just a convenience method, so you don't need to know the item's
        name -- the item name in these single-item controls is usually
        something meaningless like "1" or "on".

        For example, if a checkbox has a single item named "on", the following
        two calls are equivalent:

        .. code-block:: python

            control.toggle("on")
            control.toggle_single()

        """  # by_label ignored and deprecated
        pass

    def toggle_single(self,
                      name=None,
                      type=None,
                      kind=None,
                      id=None,
                      nr=None,
                      by_label=None,
                      label=None):  # deprecated
        """Toggle selected state of list item in control having only one item.

        The rest is as for :meth:`mechanize.HTMLForm.set_single()`

        """  # by_label ignored and deprecated
        pass

# ---------------------------------------------------
# Form-filling method applying only to FileControls.

    def add_file(self,
                 file_object,
                 content_type=None,
                 filename=None,
                 name=None,
                 id=None,
                 nr=None,
                 label=None):
        """Add a file to be uploaded.

        :arg file_object: file-like object (with read method) from which to
            read data to upload
        :arg content_type: MIME content type of data to upload
        :arg filename: filename to pass to server

        If filename is None, no filename is sent to the server.

        If content_type is None, the content type is guessed based on the
        filename and the data from read from the file object.

        At the moment, guessed content type is always application/octet-stream.

        Note the following useful HTML attributes of file upload controls (see
        HTML 4.01 spec, section 17):

          * `accept`: comma-separated list of content types
             that the server will handle correctly;
             you can use this to filter out non-conforming files
          * `size`: XXX IIRC, this is indicative of whether form
             wants multiple or single files
          * `maxlength`: XXX hint of max content length in bytes?

        """
        pass

# ---------------------------------------------------
# Form submission methods, applying only to clickable controls.

    def click(self,
              name=None,
              type=None,
              id=None,
              nr=0,
              coord=(1, 1),
              request_class=_request.Request,
              label=None):
        """Return request that would result from clicking on a control.

        The request object is a mechanize.Request instance, which you can pass
        to mechanize.urlopen.

        Only some control types (INPUT/SUBMIT & BUTTON/SUBMIT buttons and
        IMAGEs) can be clicked.

        Will click on the first clickable control, subject to the name, type
        and nr arguments (as for find_control).  If no name, type, id or number
        is specified and there are no clickable controls, a request will be
        returned for the form in its current, un-clicked, state.

        IndexError is raised if any of name, type, id or nr is specified but no
        matching control is found.  ValueError is raised if the HTMLForm has an
        enctype attribute that is not recognised.

        You can optionally specify a coordinate to click at, which only makes a
        difference if you clicked on an image.

        """
        pass

    def click_request_data(self,
                           name=None,
                           type=None,
                           id=None,
                           nr=0,
                           coord=(1, 1),
                           request_class=_request.Request,
                           label=None):
        """As for click method, but return a tuple (url, data, headers).

        You can use this data to send a request to the server.  This is useful
        if you're using httplib or urllib rather than mechanize.  Otherwise,
        use the click method.

        """
        pass

    def click_pairs(self,
                    name=None,
                    type=None,
                    id=None,
                    nr=0,
                    coord=(1, 1),
                    label=None):
        """As for click_request_data, but returns a list of (key, value) pairs.

        You can use this list as an argument to urllib.urlencode.  This is
        usually only useful if you're using httplib or urllib rather than
        mechanize.  It may also be useful if you want to manually tweak the
        keys and/or values, but this should not be necessary.  Otherwise, use
        the click method.

        Note that this method is only useful for forms of MIME type
        x-www-form-urlencoded.  In particular, it does not return the
        information required for file upload.  If you need file upload and are
        not using mechanize, use click_request_data.
        """
        pass

# ---------------------------------------------------

    def find_control(self,
                     name=None,
                     type=None,
                     kind=None,
                     id=None,
                     predicate=None,
                     nr=None,
                     label=None):
        """Locate and return some specific control within the form.

        At least one of the name, type, kind, predicate and nr arguments must
        be supplied.  If no matching control is found, ControlNotFoundError is
        raised.

        If name is specified, then the control must have the indicated name.

        If type is specified then the control must have the specified type (in
        addition to the types possible for <input> HTML tags: "text",
        "password", "hidden", "submit", "image", "button", "radio", "checkbox",
        "file" we also have "reset", "buttonbutton", "submitbutton",
        "resetbutton", "textarea", "select").

        If kind is specified, then the control must fall into the specified
        group, each of which satisfies a particular interface.  The types are
        "text", "list", "multilist", "singlelist", "clickable" and "file".

        If id is specified, then the control must have the indicated id.

        If predicate is specified, then the control must match that function.
        The predicate function is passed the control as its single argument,
        and should return a boolean value indicating whether the control
        matched.

        nr, if supplied, is the sequence number of the control (where 0 is the
        first).  Note that control 0 is the first control matching all the
        other arguments (if supplied); it is not necessarily the first control
        in the form.  If no nr is supplied, AmbiguityError is raised if
        multiple controls match the other arguments.

        If label is specified, then the control must have this label.  Note
        that radio controls and checkboxes never have labels: their items do.

        """
        pass

# ---------------------------------------------------
# Private methods.

    def _find_list_control(self,
                           name=None,
                           type=None,
                           kind=None,
                           id=None,
                           label=None,
                           nr=None):
        pass

    def _find_control(self, name, type, kind, id, label, predicate, nr):
        pass

    def _click(self,
               name,
               type,
               id,
               label,
               nr,
               coord,
               return_type,
               request_class=_request.Request):
        pass

    def _pairs(self):
        """Return sequence of (key, value) pairs suitable for urlencoding."""
        pass

    def _pairs_and_controls(self):
        """Return sequence of (index, key, value, control_index)
        of totally ordered pairs suitable for urlencoding.

        control_index is the index of the control in self.controls
        """
        pass

    def _request_data(self):
        """Return a tuple (url, data, headers)."""
        pass

    def _switch_click(self, return_type, request_class=_request.Request):
        # This is called by HTMLForm and clickable Controls to hide switching
        # on return_type.
        pass
