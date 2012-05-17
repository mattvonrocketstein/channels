""" channels/tests/test_simple.py
"""
from unittest2 import TestCase

from channel import Channel, declare_callback
from channel import CallbackError, UnboundChannel

class SimpleTests(TestCase):
    """ These tests are more or less complete for simple dictionaries. """
    def setUp(self):
        self.exchange = {}
        self.main = Channel.MAIN
        def callback(*args, **kargs): self.called_with=[args, kargs]
        self.callback = callback
        self.called_with=None

    def tearDown(self):
        self.main.bind(self.exchange)
        self.main.destroy()

    def test_channels_cached(self):
        self.assertEqual(self.main, Channel.MAIN,
                         "should not have created a new channel "+\
                         "when one of the same name already exists")
    def test_bind(self):
        self.main.bind(self.exchange)
        self.assertEqual(self.main._exchange,
                         self.exchange,
                         'expected bind would set the exchange for channel')


    def test_subscribers(self):
        with self.assertRaises(UnboundChannel):
            self.main.subscribers()
        self.main.bind(self.exchange)
        self.assertEqual(self.main.subscribers(),[],
                         'virgin channel should have no susbcribers')

    def test_subscribe(self):
        self.main.bind(self.exchange)
        def f(**kargs): pass
        self.main.subscribe(self.callback)
        self.assertEqual([self.callback],
                         self.main.subscribers(),
                         'subscription failed to propogate')
        self.main('testing')
        self.assertEqual([(self.main.name, 'testing'),{}],
                         self.called_with,
                         'subscriber was not notified')
        self.main.unsubscribe(self.callback)
        self.assertEqual(self.main.subscribers(),[],
                         'unsubscription did not take effect')

    def test_subchannels(self):
        self.main.bind(self.exchange)
        subchan = self.main.sub
        self.assertEqual(self.main.subchannels(),
                         [subchan],
                         'subchan did not show in subchannels() enumeration')
        subchan.subscribe(self.callback)
        subchan('testing')
        self.assertEqual([(subchan.name, 'testing'),{}],
                         self.called_with)