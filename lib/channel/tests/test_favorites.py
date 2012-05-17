""" channel.tests.test_favorites
"""
import copy
from unittest2 import TestCase

from channel import Channel


class TestFavorites(TestCase):
    def test_foo(self):
        exchange = {}
        channel  = Channel.main
        channel.bind(exchange)
        class Person:
            def listen_to(self,other): other.vox.subscribe(self.ear)

        def ear(*args, **kargs): print args, kargs
        alice = Person(); alice.name='alice'
        bob   = Person(); bob.name = 'bob'
        alice.vox = getattr(channel, 'alice')
        bob.vox   = getattr(channel, 'bob')
        bob.ear = copy.copy(ear)
        bob.listen_to(alice)

if __name__=='__main__':
    import unittest2; unittest2.main()
