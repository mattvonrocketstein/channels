""" channels
"""

class UnboundChannel(Exception): pass
class CallbackError(Exception): pass

class ChannelType(type):
    """ metaclass for channels """

    def __getattr__(kls, name):
        """ only attributes not starting with
            "_" are organized in the tree
        """
        FORBIDDEN = ['trait_names', # used by ipython tab completion
                     'bound','bind',
                     'subscribe', 'subscribers',
                     'unsubscribe', 'unsubscribe_all',
                     'subchannels',
                     '_getAttributeNames']
        ## This is the main channel class, accesses
        ## to it mean the accessor wants a new channel
        #  named ``name``.
        if kls.__name__=='Channel':
            if name not in FORBIDDEN and not name.startswith("_"):
                namespace = dict(_label=name,)
                bases     = (channel, )
                mcls      = kls.__metaclass__
                return kls.__metaclass__.__new__(mcls, name, bases, namespace)
            raise AttributeError("ChannelType: %r has no attribute %s" % (kls.__name__, name))

        ## This is a class with Channel somewhere in it's ancestry,
        ## if it's bound, then make a bound subchannel, otherwise yell
        else:
            if kls._bound:
                if name in FORBIDDEN or '(' in name:
                    raise AttributeError("ChannelType: %r has no attribute %s" % (kls.__name__, name))
                subchan = getattr(channel, kls._label + '::' + name)
                subchan.bind(kls._exchange)
                return subchan
            else:
                raise UnboundChannel("cannot subchannel an unbound channel")

    def __new__(mcls, name, bases, dct):
        """ called when initializing (configuring)
            class, this method caches known instances
        """

        # Don't mess with the abstract class.
        if name=='Channel':
            return type.__new__(mcls, name, bases, dct)

        # For everything else, create it or grab it from the cache
        reg = getattr(mcls, 'registry', {})
        dct.update(dict(_bound=False))
        if name not in reg: reg[name] = type.__new__(mcls, name, bases, dct)
        else:               return reg[name]
        mcls.registry = reg
        return reg[name]

    def __call__(kls, *args, **kargs):
        """ shortcut for _publish """
        return kls._publish(*args, **kargs)

    @property
    def bound(self):
        return self._bound

    @property
    def name(kls):
        return kls.__name__.split('.')[-1]

    def __repr__(self):
        return '<CHAN-({c})>'.format(c=self.__name__)

def F(msg):
    """ makes a call-only-if-bound classmethodified
        function that, if the channel is unbound, displays
        error message ``msg`` instead of running ``func``
    """
    def if_bound(func):
        def new(kls, *args, **kargs):
            if kls._bound:
                try:
                    return func(kls, *args, **kargs)
                except Exception,e:
                    raise
            else:
                raise UnboundChannel, msg
        return classmethod(new)
    return if_bound

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
        kargs.update(dict(args=args))
        exchange = kls._exchange
        func = getattr(exchange, 'publish', None)
        if func is None:
            def func(chanName, **msg):
                [sub(**msg) for sub in exchange[chanName] ]
        return func(kls._label, **kargs)

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
        [ kls.unsubscribe(subscriber) for subscriber in kls.subscribers() ]

    @classmethod
    def destroy(kls):
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

channel=Channel

class ChannelManager(object):
    @classmethod
    def enumerate_embedded_channels(kls):
        """ derives the channels embedded
            in this kls by way of inspection
        """
        CHANNELS = getattr(kls, 'CHANNELS', [])
        if CHANNELS: return CHANNELS
        matches = []
        for name in dir(kls):
            obj = getattr(kls, name)
            if hasattr(obj,'_bound'): #HACK
                matches.append(obj)
        return matches

    def bind_embedded_channels(self):
        for chan in self.enumerate_embedded_channels():
            chan.bind(self)

def verify_callback(callback):
    """ ensure callback has a signature similar
        to one of these:
            def callback(ctx, **data):       stuff()
            def callback(self, ctx, **data): stuff()
    """
    import pep362
    import inspect
    try:
      s=pep362.signature(callback)
    except AttributeError: #used declare_channel?
      s=pep362.signature(callback.fxn)

    not_more_than2 = lambda s: len(s._parameters) < 3
    if2then_self_is_one = lambda s: ( len(s._parameters)!=2 and \
                                      True ) or \
                                    ( len(s._parameters)==2 and  \
                                      'self' in s._parameters ) or \
                                    False
    at_least_one = lambda s: len(s._parameters)>0
    tests=[ s.var_args,
            not_more_than2(s),
            if2then_self_is_one(s),
            #at_least_one(s),
            s.var_kw_args ]
    if not all(tests):
       raise CallbackError('callback@{name} needs to accept *args and **kargs'.format(name=s.name))

# TODO: move this into core.channels and formalize it
# standard unpacking method: special name "args" and everything but "args"
unpack = lambda data: ( data['args'],
                        dict([ [d,data[d]] for d in data if d!='args']) )

def declare_callback(channel=None):
    assert channel,"declare_callback decorator requires 'channel' argument"
    def decorator(fxn):
        fxn.declared_callback=1
        def bootstrap(self):
            if hasattr(self, 'subscribed'):
                return False
            else:
                exchange = ChannelType.registry[channel]
                self.subscribed = 1
                k = new.instancemethod(fxn, self, self.__class__)
                setattr(self, fxn.__name__, k)
                exchange.subscribe(k)
                return self

        def new_function(self, ctx, **data):
            return fxn(self, ctx, **data)

        new_function.bootstrap=bootstrap
        new_function.declared_callback=1
        return new_function
    return decorator

def is_declared_callback(fxn):
    return hasattr(fxn, 'declared_callback')
import new
