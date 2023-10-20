# -*- encoding: utf-8 -*-
# src/astro/collective.py


from src.utils.os import log_error, log_info, log_debug, send_request, pprint


def get_collective_forecast_today(env_vars):

    api_key = env_vars['API_KEY']
    usr_id = env_vars['USER_ID']
    endpoint = 'tropical_transits/monthly'
    url = 'https://json.astrologyapi.com/v1/' + endpoint
    astro_data = {
        'day': 6,
        'month': 1,
        'year': 2000,
        'hour': 7,
        'min': 45,
        'lat': 19.132,
        'lon': 72.342,
        'tzone': 5.5,
    };
    auth = (usr_id, api_key)

    response = send_request(url, astro_data, auth)
    pprint(response)

    



