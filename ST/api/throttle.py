from django.core.cache import cache
print(cache)
##if cache is disabled throttling wont work,Throttle counts requests, cache stores the count.

from rest_framework.throttling import SimpleRateThrottle

class CustomThrottle(SimpleRateThrottle):
    scope="custom"

    def get_cache_key(self,request,view):
        return "randomanduniquestring"