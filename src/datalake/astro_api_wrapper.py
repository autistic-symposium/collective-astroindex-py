# -*- encoding: utf-8 -*-
# src/datalake/AstrologyAPIWrapper.py


import src.utils.net as net
import src.utils.os as os


class AstrologyAPIWrapper:

    def __init__(self, env_vars) -> None:

        self.env_vars = env_vars
        self.timespace = {}


    #############################  
    #       Private methods     #
    #############################

    def _retrieve_timespace(self, data) -> dict:

        if not 'city' in data or not 'country' in data:
            data['city'], data['country'] = net.get_city_and_country_from_ip()
                                 
        if not 'lat' in data or not 'lon' in data:
            data['lat'], data['lon'] = \
                            net.get_lat_and_lon_at_given_city(data['city'], data['country'])
        os.log_debug(f'Using coordinates {data["lat"]}, {data["lon"]}')

        if not 'tzone' in data:
            data['tzone_name'], data['tzone'] = \
                            net.get_timezone_offset_at_given_location(data['lat'], data['lon'])
            os.log_debug(f'Using timezone {data["tzone_name"]} with offset {data["tzone"]}')

        if not 'day' in data or \
           not 'month' in data or \
           not 'year' in data or \
           not 'hour' in data or \
           not 'mins' in data:
                data['day'], data['month'], data['year'], data['hour'], data['mins'] = \
                            net.get_datetime_now_at_given_timezone(data['tzone_name'])
        os.log_debug(f'Date {data["day"]}-{data["month"]}-{data["year"]} {data["hour"]}:{data["mins"]}')

        data['house_system'] = 'whole_sign'
        self.timespace = data 


    def _craft_request(self, endpoint, data=None) -> dict:

        data = {} if not data else data
        self._retrieve_timespace(data)

        api_key = self.env_vars['API_KEY']
        usr_id = self.env_vars['USER_ID']
        url = net.compose_url(self.env_vars['API_URL'], endpoint)
        os.log_debug(f'Requesting URL {url}')

        return net.send_request(url, self.timespace, auth=(usr_id, api_key))


    #############################  
    #  Public methods: General  #
    #############################
    
    def get_request_date(self) -> dict:

        fmt_string  = "%Y-%m-%d_%H-%M-%S"
        return net.get_date_from_timezone(self.timespace['tzone_name']).strftime(fmt_string)


    #############################  
    #  Public methods: Endpoints  #
    #############################

    def request_transits_daily(self, data=None) -> dict:
        """   Response example:
            {
            "transit_date": "17-6-2017",
            "ascendant": "Leo",
            "transit_house": [
                {
                    "planet": "Sun",
                    "natal_sign": "Taurus",
                    "transit_house": 11,
                    "is_retrograde": false
                },],
            "transit_relation": [
                {
                    "transit_planet": "Sun",
                    "natal_planet": "Jupiter",
                    "type": "Sextile",
                    "orb": 0.66
                },],
                "retrogrades": [],
                "moon_phase": null
            }
        """

        endpoint = 'tropical_transits/daily'
        return self._craft_request(endpoint, data)


    def request_transits_monthly(self, data=None) -> dict:
        """    Response example:
            {
                "month_start_date": "1-6-2017",
                "month_end_date": "30-6-2017",
                "ascendant": "Leo",
                "transit_relation": [
                    {
                        "transit_planet": "Mars",
                        "natal_planet": "Moon",
                        "type": "Trine",
                        "orb": 3.84,
                        "date": "1-6-2017"
                    },],
                "retrogrades": [],
                "moon_phase": [
                    {
                        "phase_type": "Full Moon",
                        "date": "2017-06-09T13:11:00.000Z",
                        "sign": "Sagittarius",
                        "house": 5
                    },]}
        """

        endpoint = 'tropical_transits/monthly'
        return self._craft_request(endpoint, data)


    def request_transits_natal_daily(self, data=None) -> dict:
        """ 
            Response example:

            {
            "transit_date": "1-25-2023",
            "ascendant": "Sagittarius",
            "transit_relation": [
                {
                    "transit_planet": "Sun",
                    "natal_planet": "Mercury",
                    "aspect_type": "Conjunction",
                    "start_time": "2023-01-23 05:57:47",
                    "exact_time": "2023-01-25 05:08:14",
                    "end_time": "2023-01-27 04:20:14",
                    "is_retrograde": false,
                    "transit_sign": "Aquarius",
                    "natal_house": 3,
                    "planet_in_signs": [
                        "Saturn"
                    ]
                },
                {
        """

        endpoint = 'natal_transits/daily'
        return self._craft_request(endpoint, data)


    def request_moon_phase(self, data=None) -> dict:
        """ 
            Response example:

            {
                "considered_date": "2-10-2017",
                "moon_phase": "Balsamic Moon",
                "significance": 
            }
        """

        endpoint = 'moon_phase_report'
        return self._craft_request(endpoint, data)

    
    def request_planet_tropical(self, data=None) -> dict:
        """
            Response example:

            [{
                    "name":"Sun",
                    "fullDegree":330.41334722167386,
                    "normDegree":0.4133472216738596,
                    "speed":1.0082712955819473,
                    "isRetro":"false",
                    "sign":"Pisces",
                    "house":6
                },
                {
                    "name":"Moon",
                    "fullDegree":114.14261905777207,
                    "normDegree":24.142619057772066,
                    "speed":12.96038356718529,
                    "isRetro":"false",
                    "sign":"Cancer",
                    "house":10
                },
        """

        endpoint = 'planets/tropical'
        return self._craft_request(endpoint, data)

    
    def request_natal_wheel(self, data=None) -> dict:
        """
            Response example:
                        {
                "status": true,
                "chart_url": "https://s3.ap-south-1"
                "msg": "Chart created successfully!"
            }
        """

        endpoint = 'natal_wheel_chart'
        return self._craft_request(endpoint, data)


    def request_chart_data(self, data=None) -> dict:
        """
            Response example:

            {
            "houses": [
                {
                    "start_degree": 138.21238,
                    "end_degree": 165.28495,
                    "sign": "Leo",
                    "house_id": 1,
                    "planets": []
                },
            "aspects": [
                {
                    "aspecting_planet": "Sun",
                    "aspected_planet": "Moon",
                    "aspecting_planet_id": 0,
                    "aspected_planet_id": 1,
                    "type": "Quincunx",
                    "orb": 0.22,
                    "diff": 149.78
                },
        
        """

        endpoint = 'western_chart_data'
        return self._craft_request(endpoint, data)


    def request_western_horoscope(self, data=None) -> dict:
        """
            Response example:
            {
                "planets": [
                    {
                        "name": "Sun",
                        "full_degree": 275.6427,
                        "norm_degree": 5.6427,
                        "speed": 1.019,
                        "is_retro": "false",
                        "sign_id": 10,
                        "sign": "Capricorn",
                        "house": 2
                    },
                "houses": [
                    {
                        "house": 1,
                        "sign": "Sagittarius",
                        "degree": 240.71431
                    },
                "ascendant": 240.71431015862024,
                "midheaven": 156.92135925483103,
                "vertex": 118.53668227404134,
                "lilith": {
                    "name": "Lilith",
                    "full_degree": 134.6796,
                    "norm_degree": 14.6796,
                    "speed": 0.1113,
                    "is_retro": "false",
                    "sign_id": 5,
                    "sign": "Leo",
                    "house": 9
                },
                "aspects": [
                    {
                        "aspecting_planet": "Sun",
                        "aspected_planet": "Mercury",
                        "aspecting_planet_id": 0,
                        "aspected_planet_id": 3,
                        "type": "Conjunction",
                        "orb": 2.66,
                        "diff": 2.66
                    },
        """

        endpoint = 'western_horoscope'
        return self._craft_request(endpoint, data)
