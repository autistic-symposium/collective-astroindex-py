# -*- encoding: utf-8 -*-
# utils/net.py

import time
import geocoder
import requests
from dateutil import tz
from datetime import datetime
from urllib.parse import urljoin
from timezonefinder import TimezoneFinder

import src.utils.os as os


def send_request(url: str, data=None, auth=None, params=None) -> dict:
    """Wrapper for requests calls."""

    if not params:
        params = {'header': 'Content-Type: application/json'}
    try:
        r = requests.post(url, data=data, auth=auth, params=params)

    except requests.exceptions.HTTPError as e:
        raise Exception(f'{url}: {e.response.text}')
    if r.status_code == 200:
        return r.json()
    else:
        os.log_error(f'Query failed: HTTP code {r.status_code}')


def get_city_and_country_from_ip() -> tuple:
    """Get city and country from user IP."""

    location = geocoder.ip('me')
    return location.city, location.country


def get_lat_and_lon_at_given_city(city: str, country: str) -> tuple:
    """Get latitude and longitude from a city and country."""

    location = geocoder.osm(f'{city}, {country}')
    return (location.lat, location.lng)


def get_date_from_timezone(tzone_name: str):
    """Get date from a timezone name"""

    return datetime.now(tz=tz.gettz(tzone_name))


def get_timezone_offset_at_given_location(lat: float, lon: float) -> (str, float):
    """Get timezone offset from UTC."""

    t = TimezoneFinder()
    tzone_name = t.timezone_at(lng=lon, lat=lat)
    tzone = get_date_from_timezone(tzone_name).strftime('%z')[0:-2]

    return tzone_name, float(tzone) if tzone[0] != '-' else -float(tzone[1:])

    
def get_local_tzone_name() -> str:
    """Get local timezone."""

    return time.strftime('%z', time.localtime())
  

def get_datetime_now_at_given_timezone(tzone_name=None) -> dict:
    """Get current time and timezone."""

    tzone_name = tzone_name if tzone_name else get_local_tzone_name()
    now = datetime.now(tz=tz.gettz(tzone_name))

    os.log_debug(f'Using timezone {tzone_name}')
    os.log_debug(f'Current time is {now}')
    
    return now.day, now.month, now.year, now.hour, now.minute


def compose_url(url, endpoint) -> str:
    """Compose url from base and endpoint."""

    return urljoin(url, endpoint)

