from __future__ import absolute_import

import re
from collections import defaultdict

from ._form_controls import HTMLForm, Label
from ._request import Request
from .polyglot import urljoin, is_string, as_unicode


class SkipControl(ValueError):
    pass


def normalize_line_endings(text):
    pass


def label_text(elem):
    pass


def parse_control(elem, parent_of, default_type='text'):
    pass


def parse_input(elem, parent_of, *a):
    pass


def parse_button(elem, parent_of, *a):
    pass


def parse_option(elem, parent_of, attrs_map):
    pass


def parse_textarea(elem, parent_of, *a):
    pass


def parse_select(elem, parent_of, *a):
    pass


def parse_forms(root, base_url, request_class=None, select_default=False, encoding=None):
    def parent_of(elem, parent_name):
        pass
    pass
