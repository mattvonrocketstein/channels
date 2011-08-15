""" tests for channels
"""
from unittest2 import TestCase

from channel import Channel, CallbackError, UnboundChannel

class SimpleTests(TestCase):
    """ These tests are more or less complete for simple dictionaries. """
    def setUp(self):
        self.exchange = {}
        self.main = Channel.MAIN
        def callback(*args, **kargs): self.called_with=[args, kargs]
        self.callback = callback

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
        with self.assertRaises(CallbackError):
            self.main.subscribe(f)
        self.main.subscribe(self.callback)
        self.assertEqual([self.callback],
                         self.main.subscribers(),
                         'subscription failed to propogate')
        self.main('testing')
        self.assertEqual([(), {'args': ('testing',)}],
                         self.called_with,
                         'subscriber was not notified')
        del self.called_with
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
        self.assertEqual([(), {'args': ('testing',)}],
                         self.called_with)
class ComplexTests(TestCase):
    """ TODO: tests for more complex exchanges
              that support subscribe(), etc
    """
if __name__=='__main__':
    import unittest2; unittest2.main()
