from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def get_country(x:float, y:float) -> dict:
    GEOLOC_FOUR = (
        Nominatim(user_agent="NE-1"),
        Nominatim(user_agent="NW-1"),
        Nominatim(user_agent="SE-1"),
        Nominatim(user_agent="SW-1")
    )
    geolocator = GEOLOC_FOUR[int(x < 0) + 2*int(y < 0)]

    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=0.1)
    location = reverse(query=f"{y}, {x}",language="fr")
    try:
        return location.raw["address"]
    except Exception as e:
        print(e)
        return None

