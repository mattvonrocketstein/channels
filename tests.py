""" tests for channels
"""
from unittest2 import TestCase

from channel import Channel, CallbackError, UnboundChannel

class Tests(TestCase):
    def setUp(self):
        self.exchange = {}
        self.main = Channel.MAIN

    def tearDown(self):
        self.main.bind(self.exchange)
        self.main.destroy()

    def test_channels_cached(self):
        self.assertEqual(self.main, Channel.MAIN,
                         "....")
    def test_bind(self):
        self.main.bind(self.exchange)
        self.assertEqual(self.main._exchange,
                         self.exchange,
                         '....')

    def test_subscribers(self):
        with self.assertRaises(UnboundChannel):
            self.main.subscribers()
        self.main.bind(self.exchange)
        self.assertEqual(self.main.subscribers(),[])

    def test_subscribe(self):
        self.main.bind(self.exchange)
        def f(**kargs): pass
        with self.assertRaises(CallbackError):
            self.main.subscribe(f)
        def g(*args, **kargs): self.called_with=[args, kargs]
        self.main.subscribe(g)
        self.assertEqual([g],
                         self.main.subscribers())
        self.main('testing')
        self.assertEqual([(), {'args': ('testing',)}],
                         self.called_with)
if __name__=='__main__':
    import unittest2; unittest2.main()
