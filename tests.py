""" tests for channels
"""
from unittest2 import TestCase

from channel import Channel

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
        self.main.bind(self.exchange)
        self.assertEqual(self.main.subscribers(),[])


if __name__=='__main__':
    import unittest2; unittest2.main()
