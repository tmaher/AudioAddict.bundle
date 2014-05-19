"""AudioAddict utility class."""

# pylint: disable=line-too-long, old-style-class, broad-except
# This is based entirely on http://tobiass.eu/api-doc.html (thanks!)

import urllib
import json
import random

class AudioAddict:
    """AudioAddict utility class."""

    def __init__(self):
        """Init. You know."""

        self.listenkey = None

        # The mobile_batch API requires a (static, global) HTTP Basic
        # username/pw on all requests.  Dumb, but whatever.
        self.auth_header = {'Authorization': 'Basic ZXBoZW1lcm9uOmRheWVpcGgwbmVAcHA='}

        self.validservices = {
                'sky': 'Sky.fm',
                'di': 'DI.fm',
                'jazzradio': 'JazzRadio.com',
                'rockradio': 'RockRadio.com'
                }
        self.apihost = 'api.audioaddict.com'
        self.service = None
        self.chanlist = []
        # Can't get AAC to play back, so MP3-only for now.
        self.validstreams = [
                'public3',
                'premium_high',
                'android_premium_high' # rockradio only
                ]
        # public3 is the only endpoint common to all services.
        self.streampref = 'public3'
        self.sourcepref = None

    def get_apihost(self, url=True, ssl=False):
        """Get the AA API host; normally used as part of a URL."""

        if url == False:
            return self.apihost

        obj = '://' + self.apihost + '/v1/'

        if ssl == True:
            obj = 'https' + obj
        else:
            obj = 'http' + obj

        return obj

    def set_listenkey(self, listenkey=None):
        """Set the listen_key."""

        self.listenkey = listenkey

    def get_listenkey(self, url=True):
        """Get the listen_key; normally used as part of a URL."""

        if self.listenkey == None:
            return ''
        elif url == False:
            return self.listenkey
        else:
            return '?listen_key=' + self.listenkey

    def is_validservice(self, serv=None):
        """Is this a valid service."""

        return serv in self.validservices

    def get_validservices(self):
        """Get list of valid services."""

        return self.validservices

    def set_service(self, serv=None):
        """Set which service we're using."""

        if not serv in self.validservices.keys():
            raise Exception('Invalid service')

        self.service = serv

    def get_service(self):
        """Get which service we're using."""

        return self.service

    def get_servicename(self, serv=None):
        """Get the name of a given service."""

        if serv == None:
            serv = self.get_service()

        if not serv in self.get_validservices().keys():
            raise Exception('Invalid service')

        return self.validservices[serv]

    def get_validstreams(self):
        """Get the list of valid streams."""

        return self.validstreams

    def get_serviceurl(self, serv=None, prefix='listen'):
        """Get the service URL for the service we're using."""

        if serv == None:
            serv = self.get_service()

        url = 'http://' + prefix + '.' + self.get_servicename(serv)
        url = url.lower()

        return url

    def set_streampref(self, stream=None):
        """Set the preferred stream."""

        if not stream in self.get_validstreams():
            raise Exception('Invalid stream')

        self.streampref = stream

    def get_streampref(self):
        """Get the preferred stream."""

        return self.streampref

    def set_sourcepref(self, source=None):
        """Set the preferred source."""

        self.sourcepref = source

    def get_sourcepref(self):
        """Get the preferred source."""

        return self.sourcepref

    def get_chanlist(self, refresh=False):
        """Get the master channel list."""

        if len(self.chanlist) < 1 or refresh == True:
            try:
                # Pull from public3 because it's the only endpoint common to
                # all services.
                data = urllib.urlopen(self.get_serviceurl() + '/' + self.get_streampref())
                self.chanlist = json.loads(data.read())
            except Exception:
                raise

        return self.chanlist

    def get_chaninfo(self, key):
        """Get the info for a particular channel."""

        chaninfo = None

        for chan in self.get_chanlist():
            if chan['key'] == key:
                chaninfo = chan.copy()

        if chaninfo == None:
            raise Exception('Invalid channel')

        return chaninfo

    def get_streamurl(self, key):
        """Generate a streamable URL for a channel."""

        channelurl = self.get_serviceurl() + '/' + self.get_streampref() + '/' + key + self.get_listenkey()

        data = urllib.urlopen(channelurl)
        sources = json.loads(data.read())

        streamurl = None

        # Look through the list for the preferred source.
        if not self.get_sourcepref() == None:
            for source in sources:
                if self.get_sourcepref() in source:
                    streamurl = source

        # If there is no preferred source or one was not found, pick at random.
        if streamurl == None:
            streamurl = (random.choice(sources))

        return streamurl

    def get_chanhist(self, key):
        """Get track history for a channel."""

        servurl = self.get_apihost() + self.get_service() + '/' + 'track_history/channel/' + str(self.get_chaninfo(key)['id'])

        data = urllib.urlopen(servurl)
        history = json.loads(data.read())

        return history

    def get_nowplaying(self, key):
        """Get current track for a channel."""

        # Normally the current song is position 0, but if an advertisement
        # was played in the public stream, it will pollute the history -
        # in that case, we pick the track from position 1.

        track = 'Unknown - Unknown'

        if not 'ad' in self.get_chanhist(key)[0]:
            track = self.get_chanhist(key)[0]['track']
        else:
            track = self.get_chanhist(key)[1]['track']

        return track

    def get_extinfo(self, serv=None, refresh=False):
        """Get extended info for a service from the batch API"""

        if serv == None:
            serv = self.get_service()

        url = self.get_apihost() + serv + "/mobile/batch_update?stream_set_key=public3"

        extinfo = JSON.ObjectFromURL(url, headers=self.auth_header, cacheTime = CACHE_1WEEK)

        return extinfo['channel_filters'][0]['channels']

    def get_chanthumb(self, serv=None, channel=None):
        """Get the thumbnail for a channel."""

        thumb = None

        for chaninfo in self.get_extinfo(serv=serv):
            if 'key' in chaninfo and chaninfo['key'] == channel:
                thumb = chaninfo['asset_url']

        return thumb
