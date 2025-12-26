from django.core.cache import cache
print(cache)
##if cache is disabled throttling wont work,Throttle counts requests, cache stores the count.

from rest_framework.throttling import SimpleRateThrottle

class CustomThrottle(SimpleRateThrottle):
    scope="custom"

    def get_cache_key(self,request,view):
        return "randomanduniquestring"
    


"""
DRF THROTTLING — ONE BOX REVISION

• Throttling limits how many requests can be made in a given time window.
• It protects APIs from abuse, bots, brute force, and heavy traffic.
• Authentication = who you are, Permission = what you can do, Throttling = how often.

BUILT-IN THROTTLES
• AnonRateThrottle → limit per IP for unauthenticated users.
• UserRateThrottle → limit per user ID for authenticated users.
• ScopedRateThrottle → different limits for different APIs using throttle_scope.

IMPORTANT RULES
• Throttling limits are NOT global by default.
• Limits are applied per user, per IP, or per scope.
• ScopedRateThrottle must be applied per view; adding it globally is unsafe.
• Same cache key = shared limit; different cache keys = fair usage.

CORE INTERNAL CONCEPT
• DRF throttling works using cache keys.
• cache_key → request timestamps → rate check → allow or block.
• Each cache key has its own counter.

CUSTOM THROTTLING
• All custom throttles extend SimpleRateThrottle.
• get_cache_key() defines how requests are grouped (MOST IMPORTANT).
• Returning None from get_cache_key() skips throttling.
• allow_request() decides whether to allow or return HTTP 429.
• get_rate() defines allowed requests per time window.
• wait() calculates Retry-After time.
• get_ident() resolves client IP correctly.
• throttle_failure() runs when request is blocked.

REAL-WORLD USAGE
• OTP throttling → per mobile number.
• Login throttling → per IP or per user.
• Role-based throttling → different limits for admin vs user.
• JWT tokens do NOT affect throttling identity.

CACHE & RESPONSE
• Throttling data is stored in cache (Redis recommended for production).
• HTTP 429 Too Many Requests confirms throttling is working.
• Retry-After header tells when client can retry.

MENTAL MODEL (REMEMBER THIS)
• Throttle = cache_key + rate + time window
"""


"""
ScopedRateThrottle Logic

Read throttle_scope from the view
Look for the same string in DEFAULT_THROTTLE_RATES
Apply that rate

->customs are created by extending SimpleRateThrottle and defining get_cache_key()(classes)
"""