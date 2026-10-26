from time import sleep
from datetime import time
from geopy.geocoders import Nominatim, Photon
from geopy.extra.rate_limiter import RateLimiter
from requests import Session
from subprocess import run
from json import loads


# TIME DIM
def int_to_time(n: int) -> time:
    """
        n = 234 -> 2:34
    """
    return time(hour=n//100, minute=n%100)

# SATELLITE DIM
def satellite_name(code: str) -> str | None:
    match code:
        case 'N20' :
            return 'NOAA-20'
        case 'N21' :
            return 'NOAA-21'
        case _:
            return ''

def satellite_name_id(code: str) -> int:
    match code:
        case 'N20':
            return 1
        case 'N21':
            return 2
        case _:
            return 0

# REGION DIM
def get_country_sh(xy: dict[str, [float]]) -> dict:
    try:
        d = run(
            [
                'transform/curl_region.sh',
                str(xy['latitude']),
                str(xy['longitude'])
            ],
            capture_output=True,
        ).stdout
        sleep(2)
        di = loads(d or "{}")
        print(di)
        return di
    except Exception as e:
        print(e)
        return {}

