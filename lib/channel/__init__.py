""" channels

     Channels work via an "exchange", and can't do much until they are bound.
     A channel is bound using chan.bind(some_exchange). An exchange can be any
     object, provided it obeys the dictionary protocol.

      >>> event._exchange
      <PostOffice-Service 174661484>
      >>> event._exchange[event.__name__]
      (<bound method Terminal.push_q of <Terminal-Service 175386220>>,)

    For a bound channel, both the channel and the exchange can answer questions
    about the subscribers.

      >>> event.subscribers()
      (<bound method Terminal.push_q of <Terminal-Service 176017164>>,)
      >>> event._exchange[event.__name__]
      (<bound method Terminal.push_q of <Terminal-Service 176017164>>,)

    You can build a subchannel on the fly:

      >>> event.foo
      <CHAN-(EVENT_T::foo)>

    Subchannels are cached and won't be created repeatedly

      >>> foo_channel = event.foo
      >>> foo_channel == event.foo
      True

    By default, subchannels get the same exchange their parent has

      >>> event.foo._exchange==event._exchange
      True

    Channels can non-recursively enumerate their subchannels

      >>> event.subchannels()
      [<CHAN-(EVENT_T::foo)>]

    Push a message into the channel by simply calling it. By default,
    channels should accept any number of arguments of any type.

      >>> event("testing")
      >>> event(str,object)

"""

from channel.exceptions import UnboundChannel, CallbackError
from channel.manager import ChannelManager
from channel.metaclasses import ChannelType
from channel._channel import Channel, channel
from channel.callbacks import Callback, declare_callback


class Message(object):
    """ not used yet """
    def __str__(self):
        return '<Message '.join(self.__dict__.keys())+'>'
    __repr__=__str__


#def declare_callback(channel=None):
"""
    assert channel,"declare_callback decorator requires 'channel' argument"
    def decorator(fxn):
        fxn.declared_callback = 1
        def bootstrap(self):
            if hasattr(self, 'subscribed'):
                return False
            else:
                exchange = channel._exchange
                self.subscribed = 1
                channel.subscribe(fxn)
                return self

        bootstrap(fxn)

        return fxn

    return decorator
    """
def is_declared_callback(fxn):
    return hasattr(fxn, 'declared_callback')

# standard unpacking method: special name "args" and everything but "args"
unpack = lambda data: ( data['args'],
                        dict([ [d,data[d]] for d in data if d!='args']) )
