""" channels.tests.test_declare_callback
"""
from unittest2 import TestCase

from channel import Channel
from channel import Callback, declare_callback
from channel import CallbackError, UnboundChannel

from channel.tests.base import BaseChannelTest

class DeclareCallbackTest(BaseChannelTest):
    def setUp(self):
        super(DeclareCallbackTest,self).setUp()
        self.main.bind(self.exchange)
        def testing(*args, **kargs):
            self.called_with = [args,kargs]
        self.test_cb = testing

    def do_test_builds_callback_instance(self, dec_arg):
        testing2 = declare_callback(dec_arg)(self.test_cb)
        self.assertTrue(isinstance(testing2, Callback))
        self.assertEqual(testing2.fxn, self.test_cb)

    def do_test_subscribes_callback(self, dec_arg):
        testing2 = declare_callback(dec_arg)(self.test_cb)
        self.main("testing")
        self.assertEqual(self.called_with,
                         [(self.main.name, 'testing'), {}])
class TestChannelType(DeclareCallbackTest):
    def test_subscribes_callback(self):
        self.do_test_subscribes_callback(self.main)

    def test_builds_callback_instance(self):
        self.do_test_builds_callback_instance(self.main)

class TestStringType(DeclareCallbackTest):
    def test_subscribes_callback(self):
        self.do_test_subscribes_callback(self.main.name)

    def test_builds_callback_instance(self):
        self.do_test_builds_callback_instance(self.main.name)

if __name__=='__main__':
    import unittest2; unittest2.main()
