"""AudioAddict utility class."""

# pylint: disable=line-too-long, old-style-class, broad-except
# This is based entirely on http://tobiass.eu/api-doc.html (thanks!)

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

        # Can't get AAC to play back, so MP3-only for now.
        self.validstreams = [
                'public3',
                'premium_high',
                'android_premium_high' # rockradio only
                ]
        # public3 is the only endpoint common to all services.
        self.streampref = 'public3'
        self.sourcepref = None

    def heat_up_cache(self, refresh=False):
        for serv in self.validservices:
            HTTP.PreCache(self.batch_update_url(serv), headers=self.auth_header)

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

    def batch_update_url(self, serv=None):
        return self.get_apihost() + serv + "/mobile/batch_update?stream_set_key=" + self.streampref

    def get_ext_channel_info(self, serv=None, channel=None, attr=None):
        """Get extended channel info from local storage"""

        if (not 'ext_chaninfo' in Dict) or (not serv in Dict['ext_chaninfo']):
            self.fetch_service_channel_info(serv)

        if not(channel in Dict['ext_chaninfo'][serv]):
            self.fetch_service_channel_info(serv, refresh=True)

        if not(channel in Dict['ext_chaninfo'][serv]):
            Log.Error("Trying to read nonexistant channel %s/%s", serv, channel)
            return None

        if attr == None:
          return Dict['ext_chaninfo'][serv][channel]

        if not attr in Dict['ext_chaninfo'][serv][channel]:
          return None

        return Dict['ext_chaninfo'][serv][channel][attr]

    def fetch_service_channel_info(self, serv=None, refresh=False):
        """Fetch from API everything we need to know about this service"""

        Log.Debug("batch_update fetch, serv %s", serv)

        max_age_in_cache = 0 if refresh else CACHE_1WEEK
        svc_info = JSON.ObjectFromURL(self.batch_update_url(serv), headers=self.auth_header, cacheTime = max_age_in_cache)

        if refresh or (not 'ext' in Dict):
            Dict['ext'] = {}
        Dict['ext'][serv] = svc_info

        if refresh or (not 'ext_chaninfo' in Dict):
            Dict['ext_chaninfo'] = {}
        if refresh or (not serv in Dict['ext_chaninfo']):
            Dict['ext_chaninfo'][serv] = {}

        for chaninfo in svc_info['channel_filters'][0]['channels']:
            Dict['ext_chaninfo'][serv][chaninfo['key']] = chaninfo

        return True


    def get_service(self):
        """Get which service we're using."""

        return self.service

    def get_servicename(self, serv=None):
        """Get the name of a given service."""

        if not serv in self.get_validservices():
            raise Exception("Invalid service %s" % serv)

        return self.validservices[serv]

    def get_validstreams(self):
        """Get the list of valid streams."""

        return self.validstreams

    def get_serviceurl(self, serv=None):
        """Get the service URL for the service we're using."""

        return 'http://listen.' + self.get_servicename(serv).lower() + '/'

    def set_streampref(self, stream=None):
        """Set the preferred stream."""

        if not stream in self.get_validstreams():
            raise Exception('Invalid stream')

        self.streampref = stream

    def set_sourcepref(self, source=None):
        """Set the preferred source."""

        self.sourcepref = source

    def get_sourcepref(self):
        """Get the preferred source."""

        return self.sourcepref

    def get_chanlist(self, serv=None, refresh=False):
        """Get the master channel list."""

        max_time_in_cache = 0 if refresh else CACHE_1HOUR

        return JSON.ObjectFromURL(self.get_serviceurl(serv) + self.streampref, cacheTime=max_time_in_cache)

    def get_chaninfo(self, serv=None, channel=None):
        """Get the info for a particular channel."""

        chaninfo = None

        for chan in self.get_chanlist(serv):
            if chan['key'] == channel:
                chaninfo = chan.copy()

        if chaninfo == None:
            raise Exception('Invalid channel')

        return chaninfo

    def get_streamurl(self, serv=None, channel=None):
        """Generate a streamable URL for a channel."""

        channelurl = self.get_serviceurl(serv) + self.streampref + '/' + channel + self.get_listenkey()

        sources = JSON.ObjectFromURL(channelurl)

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

    def get_chanhist(self, serv=None, channel=None):
        """Get track history for a channel."""

        servurl = self.get_apihost() + serv + '/track_history/channel/' + str(self.get_chaninfo(serv, channel)['id'])

        return JSON.ObjectFromURL(servurl, cacheTime=0)

    def get_nowplaying(self, serv=None, channel=None):
        """Get current track for a channel."""

        # Normally the current song is position 0, but if an advertisement
        # was played in the public stream, it will pollute the history -
        # in that case, we pick the track from position 1.

        track = 'Unknown - Unknown'

        if not 'ad' in self.get_chanhist(serv, channel)[0]:
            track = self.get_chanhist(serv, channel)[0]['track']
        else:
            track = self.get_chanhist(serv, channel)[1]['track']

        return track

    def get_chanthumb(self, serv=None, channel=None):
        """Get the thumbnail for a channel."""

        return self.get_ext_channel_info(serv, channel, attr='asset_url')
