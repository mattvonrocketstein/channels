Channels work via an "exchange", and can't do much until
they are bound.  A channel is bound using chan.bind(some_exchange).
Exchanges can be any object, provided they obeys the dictionary protocol.

      >>> event._exchange
      <PostOffice-Service 174661484>
      >>> event._exchange[event.__name__]
      (<bound method Terminal.push_q of <Terminal-Service 175386220>>,)

For a bound channel, both the channel and the exchange can answer
questions about the subscribers

      >>> event.subscribers()
      (<bound method Terminal.push_q of <Terminal-Service 176017164>>,)
      >>> event._exchange[event.__name__]
      (<bound method Terminal.push_q of <Terminal-Service 176017164>>,)

You can build a subchannel on the fly

      >>> event.foo
      <CHAN-(EVENT_T::foo)>

Subchannels are cached

      >>> foo_channel = event.foo
      >>> foo_channel == event.foo
      True

By default subchannels get the same exchange their parent has

      >>> event.foo._exchange==event._exchange
      True

Channels can non-recursively enumerate their subchannels

      >>> event.subchannels()
      [<CHAN-(EVENT_T::foo)>]

Push a message into the channel by simply calling it. by default,
channels should accept any number of arguments of any type.

      >>> event("testing")
      >>> event(str,object)
