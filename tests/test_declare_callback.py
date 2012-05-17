""" channels/tests/test_declare_callback.py
"""
from unittest2 import TestCase

from channel import Channel, declare_callback
from channel import CallbackError, UnboundChannel
from .test_simple import SimpleTests
class DeclareCallbackTest(SimpleTests):
    def test_decorator(self):
        self.main.bind(self.exchange)
        @declare_callback(self.main)
        def testing(*args, **kargs):
            self.called_with = [args,kargs]
        self.main("testing")
        self.assertEqual(self.called_with,
                         [(self.main.name, 'testing'),{}])
