""" channel.metaclasses
"""

from channel.exceptions import UnboundChannel


class ChannelType(type):
    """ metaclass for channels """

    def __getattr__(kls, name):
        """ only attributes not starting with "_" are organized in the tree
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
        from channel._channel import Channel
        if kls.__name__=='Channel':
            if name not in FORBIDDEN and not name.startswith("_"):
                namespace = dict(_label=name,)
                bases     = (Channel, )
                mcls      = kls.__metaclass__
                return kls.__metaclass__.__new__(mcls, name, bases, namespace)
            raise AttributeError("ChannelType: %r has no attribute %s" % (kls.__name__, name))

        ## This is a class with Channel somewhere in it's ancestry,
        ## if it's bound, then make a bound subchannel, otherwise yell
        else:
            #raise Exception,'NIY'
            if kls._bound:
                if name in FORBIDDEN or '(' in name:
                    err = "ChannelType: %r has no attribute %s" % (kls.__name__, name)
                    raise AttributeError(err)
                subchan = getattr(Channel, kls._label + '::' + name)
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
        """ """
        return self._bound

    @property
    def name(kls):
        """ """
        return kls.__name__.split('.')[-1]

    def __repr__(self):
        """ """
        return '<CHAN-({c})>'.format(c=self.__name__)
