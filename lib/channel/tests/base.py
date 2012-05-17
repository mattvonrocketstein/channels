""" channels.tests.base
"""
from unittest2 import TestCase

from channel import Channel, declare_callback
from channel import CallbackError, UnboundChannel

class BaseChannelTest(TestCase):
    def setUp(self):
        """ does not bind exchange, does not subscribe callback.
            individual methods will have to handle all that stuff
            but at least everything is ready for them already
        """
        self.exchange = {}
        self.main = Channel.MAIN
        def callback(*args, **kargs): self.called_with=[args, kargs]
        self.callback = callback
        self.called_with=None

    def tearDown(self):
        """ cannot destroy an unbound channel? """
        self.main.bind(self.exchange)
        self.main.destroy()
