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


def get_lat_and_lon_at_given_city(city: str, country: str) -> tuple:
    """Get latitude and longitude from a city and country."""

    if not city or not country:
        os.log_info('No city or country provided. Using user IP location.')

        location = geocoder.ip('me')
    else:
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


def get_timespace_dict(day=None, month=None, year=None, hour=None, mins=None, lat=None, \
                  lon=None, tzone=None, city=None, country=None) -> dict:
    """Craft data to send to the API."""

    if not lat or not lon:
        lat, lon = get_lat_and_lon_at_given_city(city, country)
    os.log_debug(f'Using coordinates {lat}, {lon}')

    if not tzone:
        tzone_name, tzone = get_timezone_offset_at_given_location(lat, lon)
        os.log_debug(f'Using timezone {tzone}')

    if not day or not month or not year or not hour or not mins:
        day, month, year, hour, mins = get_datetime_now_at_given_timezone(tzone_name)
    os.log_debug(f'Using date {day}/{month}/{year} {hour}:{mins}')

    return {
        'day': day,
        'month': month,
        'year': year,
        'hour': hour,
        'min': mins,
        'lat': lat,
        'lon': lon,
        'tzone': tzone,
        'tzone_name': tzone_name
    }    

    
def craft_request(env_vars, endpoint, data, custom_data=None) -> dict:
    """Send request to a designed endpoint in the API."""

    if custom_data:
        data.update(custom_data)

    api_key = env_vars['API_KEY']
    usr_id = env_vars['USER_ID']
    url = urljoin(env_vars['API_URL'], endpoint)
    os.log_debug(f'Requesting URL {url}')

    return send_request(url, data, auth=(usr_id, api_key))


