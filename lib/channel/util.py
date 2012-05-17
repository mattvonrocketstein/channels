""" channel.util
"""
from .exceptions import UnboundChannel
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
                raise UnboundChannel(msg)
        return classmethod(new)
    return if_bound
