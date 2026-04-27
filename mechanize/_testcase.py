from __future__ import absolute_import
import os
import shutil
import tempfile
import unittest


class SetupStack(object):
    def __init__(self):
        self._on_teardown = []

    def add_teardown(self, teardown):
        pass

    def tear_down(self):
        pass


class TearDownConvenience(object):
    def __init__(self, setup_stack=None):
        pass

    # only call this convenience method if no setup_stack was supplied to c'tor
    def tear_down(self):
        pass


class TempDirMaker(TearDownConvenience):
    def make_temp_dir(self, dir_=None):
        pass


class MonkeyPatcher(TearDownConvenience):

    Unset = object()

    def monkey_patch(self, obj, name, value):
        pass

    def _set_environ(self, env, name, value):
        pass

    def monkey_patch_environ(self, name, value, env=os.environ):
        pass


class FixtureFactory(object):
    def __init__(self):
        self._setup_stack = SetupStack()
        self._context_managers = {}
        self._fixtures = {}

    def register_context_manager(self, name, context_manager):
        pass

    def get_fixture(self, name, add_teardown):
        pass

    def get_cached_fixture(self, name):
        pass

    def tear_down(self):
        pass


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def register_context_manager(self, name, context_manager):
        pass

    def get_fixture(self, name):
        pass

    def get_cached_fixture(self, name):
        pass

    def add_teardown(self, *args, **kwds):
        pass

    def make_temp_dir(self, *args, **kwds):
        pass

    def monkey_patch(self, *args, **kwds):
        pass

    def monkey_patch_environ(self, *args, **kwds):
        pass

    def assert_contains(self, container, containee):
        pass

    def assert_less_than(self, got, expected):
        pass
