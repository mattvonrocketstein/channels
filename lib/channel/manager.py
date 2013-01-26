""" channel.manager
"""

from channel.metaclasses import ChannelType
from channel._channel import Channel
from channel.exceptions import ChannelExists

class ChannelManager(object):
    """ """

    @classmethod
    def enumerate_embedded_channels(kls):
        """ derives the channels embedded
            in this kls by way of inspection

            TODO: use goulash
            TODO: should this really be a classmethod?
        """
        CHANNELS = getattr(kls, 'CHANNELS', [])
        if CHANNELS: return CHANNELS
        matches = []
        for name in dir(kls):
            if name.startswith('__'): continue
            obj = getattr(kls, name)
            if isinstance(obj, ChannelType):
                matches.append(obj)
        return matches

    def add_channel(self, name):
        """ """
        if hasattr(self.__class__, name):
            raise ChannelExists(name)
        else:
            chan = getattr(Channel, name)
            setattr(self.__class__,name, chan)
            chan.bind(self)
            return chan

    def bind_embedded_channels(self):
        for chan in self.enumerate_embedded_channels():
            chan.bind(self)
