""" channel._channel
"""

from channel.util import F
from channel.metaclasses import ChannelType
from channel.callbacks import verify_callback

class Channel(object):
    """
        TODO: channel type declarations.. use linda?
    """

    __metaclass__ = ChannelType

    @F("cannot publish subscribers for an unbound channel")
    def subscribers(kls):
        return kls._exchange[kls._label]

    @F("cannot subscribe to an unbound channel")
    def subscribe(kls, callback):
        verify_callback(callback)
        exchange = kls._exchange
        func = getattr(exchange, 'subscribe', None)
        if func is None:
            def func(chanName, subscriber):
                exchange[chanName] += [subscriber]
        return func(kls._label, callback)

    @F("cannot publish to a unbound channel")
    def _publish(kls, *args, **kargs):
        assert 'args' not in kargs,"'args' is reserved for internal use"
        #kargs.update(dict(args=args))
        exchange = kls._exchange
        func = getattr(exchange, 'publish', None)
        if func is None:
            chanName = kls.name
            #print 'none'
            #from IPython import Shell; Shell.IPShellEmbed(argv=['-noconfirm_exit'])()
            def func(*args1, **kargs1):
                [sub(*args1, **kargs1) for sub in exchange[chanName] ]
        try:
            return func(kls._label, *args, **kargs)
        except TypeError:
            print 'terrer'
            from IPython import Shell; Shell.IPShellEmbed(argv=['-noconfirm_exit'])()

    @classmethod
    def unsubscribe(kls, subscriber):
        """ """
        exchange = kls._exchange
        func = getattr(exchange, 'unsubscribe', None)
        if func is None:
            def func(chanName, subscriber):
                exchange[chanName] = [x for x in exchange[chanName] if x!=subscriber]
        func(kls._label, subscriber)

    @classmethod
    def unsubscribe_all(kls):
        """ """
        [ kls.unsubscribe(subscriber) for subscriber in kls.subscribers() ]

    @classmethod
    def destroy(kls):
        """ """
        kls.unsubscribe_all()
        del Channel.__metaclass__.registry[kls._label]
        return None

    @F("cannot query for subchannels on an unbound channel")
    def subchannels(kls):
        return [ item[1] for item in Channel.registry.items() \
                 if item[0].startswith(kls._label+'::') ]

    @classmethod
    def bind(kls, postoffice):
        """ a channel must be bound to operate """
        postoffice[kls._label] = [] # FIXME
        kls._bound      = True
        kls._exchange = postoffice
        return kls
channel = Channel
