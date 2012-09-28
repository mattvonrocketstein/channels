""" channel.tests.test_favorites
"""
import copy

from unittest2 import TestCase

from channel import Channel

class Person:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<{0}>'.format(self.name.title())

    @property
    def vox(self):
        return getattr(self.channel, self.name)

    def listen_to(self, other):
        other.vox.subscribe(self.ear)

    def ear(self, *args, **kargs):
        print self.name, 'receiving', args, kargs

class TestFavorites(TestCase):
    def setUp(self):
        exchange = {}
        channel  = Channel.main
        channel.bind(exchange)
        self.alice = Person('self.alice')
        self.bob   = Person('self.bob')
        self.alice.vox = getattr(channel, 'self.alice')
        self.bob.vox   = getattr(channel, 'self.bob')

    def test_1(self):
        self.bob.listen_to(self.alice)
        self.assertTrue(self.bob.ear in self.alice.vox.subscribers())
