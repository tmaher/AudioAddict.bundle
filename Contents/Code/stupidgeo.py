"""Geolocation utility class"""

from math import radians, cos, sin, asin, sqrt
from urlparse import urlparse

class StupidGeo:
    """Geolocation utility class"""

    def __init__(self):
        self.lookup_url = "https://freegeoip.net/json/"

    def get_location_info(self, target="", cacheTime=CACHE_1WEEK):
        """
        Get lat/lon & other useful info for a given IP/hostname.
        See http://freegeoip.net/ for more info.  Result looks like...

        {
          "ip":"79.141.174.3",
          "country_code":"DE", "country_name":"Germany",
          "region_code":"05", "region_name":"Hessen",
          "city":"Frankfurt Am Main", "zipcode":"",
          "latitude":50.1167,"longitude":8.6833,
          "metro_code":"", "area_code":""
        }
        """

        # We don't do any explicit caching here because we can just
        # rely on Plex's HTTP cache.
        return JSON.ObjectFromURL(self.lookup_url + self.norm_hostname(target),
                                  cacheTime=cacheTime)

    def norm_hostname(self, name_or_url):
        """
        Given either an URL or hostname, return just the hostname.

        urlparse("www.google.com").hostname returns a Python NoneType object,
        so, yeah, this is necessary.
        """

        url_hostname = urlparse(name_or_url).hostname
        return name_or_url if url_hostname == None else url_hostname

    def get_closest_host(self, candidates, target=""):
        """
        Given a list of candidate IP/hostnames and a single target,
        find the candidate with the closest Haversine distance.
        """

        t = self.get_location_info(target)
        return min(candidates,
            key=lambda x: self.haversine(t, self.get_location_info(x['url'])))

    def haversine(self, pos1, pos2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        Cribbed from https://stackoverflow.com/questions/4913349/
        """

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians,
            [pos1['longitude'], pos1['latitude'],
             pos2['longitude'], pos2['latitude']])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))

        # 6367 km is the radius of the Earth
        km = 6367 * c
        return km
