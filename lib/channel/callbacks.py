""" channel.callbacks
"""

import pep362
import inspect

from channel.metaclasses import ChannelType

class Callback(object):
    def __init__(self, fxn):
        self.fxn = fxn

class declare_callback(object):
    def __init__(self, channelish):
        dispatch_to = 'handle_' + type(channelish).__name__.lower()
        getattr(self, dispatch_to)(channelish)

    def handle_str(self, chan_name):
        """ got a string.  hopefully it's a channel name,
            so we'll look up the channel from the registry
        """
        return self.handle_channeltype(ChannelType.registry[chan_name])

    def handle_channeltype(self, chan):
        """ easy, we got handed a channel directly. """
        self.channel = chan

    def __call__(self, fxn):
        cb = Callback(fxn)
        self.channel.subscribe(fxn)
        return cb

def verify_callback(callback):
    """ ensure callback has a signature similar
        to one of these:
            def callback(ctx, **data):       stuff()
            def callback(self, ctx, **data): stuff()
    """
    try:
      s = pep362.signature(callback)
    except AttributeError: #used declare_channel?
      s = pep362.signature(callback.fxn)

    not_more_than2 = lambda s: len(s._parameters) < 3
    if2then_self_is_one = lambda s: ( len(s._parameters)!=2 and True ) or \
                                    ( len(s._parameters)==2 and 'self' in s._parameters )

    at_least_one = lambda s: len(s._parameters) > 0
    if not s.var_args:
       # maybe warn them or something here..
       pass
    tests = [ #s.var_args,
              not_more_than2(s),
              if2then_self_is_one(s),
              #at_least_one(s),
               ]

    if not s.var_kw_args: #all(tests):
       err='callback@{name} needs to accept **kargs'
       raise CallbackError(err.format(name=s.name))
