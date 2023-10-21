# -*- encoding: utf-8 -*-
# src/analytics/collective.py

import time
import yaml



from urllib.parse import urljoin


import src.utils.os as os
import src.utils.net as net





def get_collective_forecast_now(env_vars):

    data = net.get_timespace(city='New York', country='USA')
    print(data)
    endpoint = 'tropical_transits/daily'
    response = net.craft_request(env_vars, endpoint, data)
    print(response)
    #

    #collective_index = 0






def test():
    pprint(astro_data)

    auth = (usr_id, api_key)

    
    pprint(response)


    houses = { i: [] for i in range(1, 13)}

    ascendant = response['ascendant']
    moon_phase = response['moon_phase']
    retrograde = response['retrogrades']
    transit_house = response['transit_house']
    transit_relation = response['transit_relation']

    for p in transit_house:
        planet = p['planet']
        transit_house = p['transit_house']
        natal_sign = p['natal_sign']
        is_retrograde = p['is_retrograde']

        print(f'{planet} is in {transit_house} in {natal_sign} and is retrograde: {is_retrograde}')

        houses[transit_house].append([planet, natal_sign, is_retrograde])

    print(houses)

    for t in transit_relation:
        planet1 = t['natal_planet']
        planet2 = t['transit_planet']
        orb = t['orb']
        transit_type = t['type']

        if planet1 != planet2:
            print(f'{planet1} is in {transit_type} with {planet2} with an orb of {orb}')


    water_house = [4, 8, 12]
    fire_house = [1, 5, 9]
    air_house = [3, 7, 11]
    earth_house = [2, 6, 10]
    investing_house = [2, 5, 8, 10, 11]

    sign_bullish = ['Taurus', 'Virgo', 'Capricorn']
    sign_bearish = ['Aries', 'Cancer', 'Libra', 'Scorpio']
    sign_neutral = ['Gemini', 'Leo', 'Sagittarius', 'Aquarius', 'Pisces']

    planet_bullish = ['Sun', 'Jupiter', 'Venus']
    planet_bearish = ['Saturn', 'Mars']
    planet_neutral = ['Mercury', 'Moon']


    for house_num, planets in houses.items():

        if house_num in investing_house:

            for planet in planets:
                if planet[0] in planet_bullish:
                    if planet[1] in sign_bullish:
                        collective_index += 15
                    elif planet[1] in sign_bearish:
                        collective_index -= 5
                    else:
                        collective_index += 10
                elif planet[0] in planet_bearish:
                    if planet[1] in sign_bullish:
                        collective_index -= 15
                    elif planet[1] in sign_bearish:
                        collective_index -= 5
                    else:
                        collective_index -= 10
        
    

    print(f'Collective Index: {collective_index}')
                    

    

    with open("intel.yaml", "r") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)