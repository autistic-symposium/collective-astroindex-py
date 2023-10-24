# -*- encoding: utf-8 -*-
# src/intel/collective.py

#TODO: move to utils
from datetime import timedelta, datetime

import src.utils.os as os
import src.utils.net as net


class CollectiveIndex:

    def __init__(self, env_vars, city=None, country=None):

        #######################
        ### Load intel YAML ###
        #######################
        self.env_vars = env_vars
        self.sentiment_ranking, self.feature_ranking = self._load_ranking()


        # TODO: clean this up
        self.collective_intel = os.load_yaml(self.env_vars['STRATEGIES_COLLECTIVE'])
        self.general_intel = os.load_yaml(self.env_vars['STRATEGIES_GENERAL'])
        self.moon_intel = os.load_yaml(self.env_vars['STRATEGIES_MOON'])

        
        self.collective_index = {}
        self.location = (city, country)
        self.timespace = net.get_timespace_dict(self.location)
        self.ascendant_now = None
        self.houses_now = {h: [] for h in range(1, 13)}
        self.planets_now = {}
        self.retrogrades_now = []
        self.moon_phase = {}

        #TODO: move this to yaml
        self.transit_now = {t: [] for t in ['conjunction', 'trine', 'square', 'opposition', 'sextile']}
        self.transit_monthly = {}
        self.transit_now_custom = {}
        self.transit_moon = {}
        self.transit_forecast = {}
        self.chart_data = {'houses': [], 'aspects': []}
        self.whole_sign_houses = {
                        'planets': [], 
                        'houses': [], 
                        'vertex': None, 
                        'midheaven': None,
                        'lilith': None,
                        'aspects': [],
                        'ascendant': None
                        }
        self.natal_chart = {
                        'planets': [],
                        'houses': [],
                        'aspects': [],
                        'ascendant': None,
                        'midheaven': None,
                        'lilith': None,
                        'vertex': None,
                        'moon_phase': [],
                        'elements': [],
                        'modes': [],
                        'dominant_signs': []
                        }

        self.transit_index = {}

        # TODO: move to a setup() func

    ####################################
    #   Private methods for Set Up
    ####################################
    def _load_ranking(self) -> None:
        """Load and parse ranking from YAML."""

        ranking = os.load_yaml(self.env_vars['STRATEGIES_RANKING'])
        sentiment_ranking = {k: float(ranking['translation'][v]) for k, v in ranking['sentiments'].items()}
        feature_ranking = {k: float(ranking['translation'][v]) for k, v in ranking['features'].items()}

        return sentiment_ranking, feature_ranking


    ##################################################
    #   Private methods for parsing the response data
    ##################################################

    def _parse_data_transits_daily(self, data: dict) -> None:
        """Parse data from transits daily."""

        ### Divide and save the data
        self.ascendant_now = data['ascendant'].lower()
        transit_house = data['transit_house']
        transit_relation = data['transit_relation']

        ### Parse the houses and planets
        for obj in transit_house:
            planet = obj['planet'].lower()
            self.planets_now[planet] = obj['natal_sign'].lower()
            self.houses_now[obj['transit_house']].append(planet)

            if bool(obj['is_retrograde']):
                self.retrogrades_now.append(planet)

        ## Print the data
        os.log_debug(f'Ascendant now: {self.ascendant_now}')
        os.log_debug(f'Signs of planets now: {self.planets_now}')
        os.log_debug(f'Planets in houses now: {self.houses_now}')
        os.log_debug(f'Retrogrades now: {self.retrogrades_now}')

        ### Get transits
        for t in transit_relation:
            planet1 = t['natal_planet'].lower()
            planet2 = t['transit_planet'].lower()
            transit_type = t['type'].lower()
            orb = float(t['orb'])

            if planet1 == planet2:
                continue
            
            self.transit_now[transit_type].append((planet1, planet2, orb))


    def _parse_data_transits_monthly(self, data: dict) -> None:
        """Parse data from transits monthly."""

        ### Divide and save the data
        # TODO: period is not used
        period = [data['month_start_date'], data['month_end_date']]
        # the moon api and retrograde api doesn't seen to be working
        moon_phase = data['moon_phase']
        retrogrades = data['retrogrades']
        transit_relation = data['transit_relation']

        ### Get transits
        for t in transit_relation:
            planet1 = t['natal_planet'].lower()
            planet2 = t['transit_planet'].lower()
            transit_type = t['type'].lower()
            orb = float(t['orb'])
            date = t['date']

            if planet1 == planet2:
                continue
            if date not in self.transit_monthly:
                self.transit_monthly[date] = [(planet1, planet2, transit_type, orb)]
            else:
                self.transit_monthly[date].append((planet1, planet2, transit_type, orb))
        
        ### Get moon phases
        # TODO: this has no data
        for m in moon_phase:
            date, time = m['date'].split('T')
            self.moon_phase[date] = (m['phase'].lower(), time, m['sign'].lower())

        ### Print the data
        os.log_debug(f'Moon phases: {self.moon_phase}')
        os.log_debug(f'Transits monthly: {self.transit_monthly}')

        # TODO: why I am getting old dates? remove them


    def _parse_data_transits_daily_custom(self, data: dict) -> None:
        """Parse data from custom transits daily."""

        ### Divide and save the data
        self.ascendant_now = data['ascendant'].lower()
        transit_date = data['transit_date']
        transit_relation = data['transit_relation']
        os.log_debug(f'Ascendant now: {self.ascendant_now}')

        ### Get transits
        for t in transit_relation:
            planet1 = t['natal_planet'].lower()
            planet2 = t['transit_planet'].lower()
            transit_type = t['aspect_type'].lower()
            this_date = t['exact_time'].split(' ')
            is_retrograde = t['is_retrograde']
            transit_sign = t['transit_sign'].lower()
            house = t['natal_house']

            if planet1 == planet2:
                continue

            # Sometimes exact time is '_'
            if len(this_date) == 1:
                start_dt, start_time = t['start_time'].split(' ')
                end_dt, end_time = t['end_time'].split(' ')

                start_y, start_m, start_d = start_dt.split('-')
                end_y, end_m, end_d = end_dt.split('-')

                start_dt = date(int(start_y), int(start_m), int(start_d))
                end_dt = date(int(end_y), int(end_m), int(end_d))

                def daterange(date1, date2):
                    for n in range(int((date2 - date1).days) + 1):
                        yield date1 + timedelta(n)

                for dt in daterange(start_dt, end_dt):
                    # TODO: fix this
                    this_date = dt.strftime("%Y-%m-%d")
                    this_date = datetime.strptime(this_date, '%Y-%m-%d').strftime('%d-%m-%Y')

            else:
                this_date = datetime.strptime(this_date[0], '%Y-%m-%d').strftime('%d-%m-%Y')
           
            # TODO: add time
            this_value = (planet1, planet2, transit_type, is_retrograde, transit_sign, house)
            if self.transit_now_custom.get(this_date):
                self.transit_now_custom[this_date].append(this_value)
            else:
                self.transit_now_custom[this_date] = [this_value]


    def _parse_data_transits_moon(self, data: dict) -> None:
        """Parse data from moon phase."""

        self.moon_phase[data['considered_date']] = data['moon_phase']
        significance = data['significance']

        print(f'Moon phase: {self.moon_phase}')
        print(f'Significance: {significance}')


    def _parse_data_transits_forecast(self, data: dict) -> None:
        """ Parse data from transit forecast."""

        for obj in data:
            planet = obj['name'].lower()
            full_degree = obj['fullDegree']
            norm_degree = obj['normDegree']
            speed = obj['speed']
            is_retrograde = obj['isRetro']
            sign = obj['sign'].lower()
            house = obj['house']
            
            if planet == 'Ascendant':
                self.ascendant_now = sign
            
            self.transit_forecast[planet] = [full_degree, norm_degree, speed, is_retrograde, sign, house]
            

    def _parse_data_wheel(self, data: dict) -> None:
        """Parse data from wheel."""

        if data['status'] == True:
            url = data['chart_url']
            os.log_info(f'Wheel created: {url}')


    def _parse_data_chart_data(self, data: dict) -> None:
        """Parse data from chart data."""

        for key, values in data.items():

            if key == 'houses':
                for value in values:
                    start_degree = value['start_degree']
                    end_degree = value['end_degree']
                    sign = value['sign'].lower()
                    house = value['house_id']
                    planets = value['planets']

                    self.chart_data['houses'].append((start_degree, end_degree, sign, house, planets))
            
            elif key == 'aspects':
                for value in values:
                    aspected_planet = value['aspected_planet'].lower()
                    aspecting_planet = value['aspecting_planet'].lower()
                    aspect = value['type'].lower()
                    orb = value['orb']
                    diff = value['diff']

                    self.chart_data['aspects'].append((aspected_planet, aspecting_planet, aspect, orb, diff))

    def _parse_data_whole_sign_houses(self, data: dict) -> None:
        """Parse data from whole sign houses."""

        for key, values in data.items():

            if key == 'planets':
                for value in values:
                    planet = value['name']
                    full_degree = value['full_degree']
                    norm_degree = value['norm_degree']
                    speed = value['speed']
                    is_retrograde = value['is_retro']
                    sign = value['sign'].lower()
                    house = value['house']

                    self.whole_sign_houses['planets'].append((planet, full_degree, norm_degree, speed, is_retrograde, sign, house))

            elif key == 'houses':
                for value in values:
                    house = value['house']
                    sign = value['sign'].lower()
                    degree = value['degree']

                    self.whole_sign_houses['houses'].append((house, sign, degree))

            elif key == 'ascendant':
                self.whole_sign_houses['ascendant'] = values

            elif key == 'midheaven':
                self.whole_sign_houses['midheaven'] = values
        
            elif key == 'vertex':
                self.whole_sign_houses['vertex'] = values

            elif key == 'lilith':
                full_degree = values['full_degree']
                norm_degree = values['norm_degree']
                speed = values['speed']
                is_retrograde = values['is_retro']
                sign = values['sign'].lower()
                house = values['house']
                
                self.whole_sign_houses['lilith'] = (full_degree, norm_degree, speed, is_retrograde, sign, house)

            elif key == 'aspects':
                for value in values:
                    aspecting_planet = value['aspecting_planet'].lower()
                    aspected_planet = value['aspected_planet'].lower()
                    aspect = value['type'].lower()
                    orb = value['orb']
                    diff = value['diff']

                    self.whole_sign_houses['aspects'].append((aspected_planet, aspecting_planet, aspect, orb, diff))


    def _parse_data_natal_chart(self, data: dict) -> None:
        """Parse data from natal chart."""

        for key, values in data.items():

            if key == 'planets':
                for value in values:
                    planet = value['name']
                    full_degree = value['full_degree']
                    norm_degree = value['norm_degree']
                    speed = value['speed']
                    is_retrograde = value['is_retro']
                    sign = value['sign'].lower()
                    house = value['house']

                    self.natal_chart['planets'].append((planet, full_degree, norm_degree, speed, is_retrograde, sign, house))

            elif key == 'houses':
                for value in values:
                    house = value['house']
                    sign = value['sign'].lower()
                    degree = value['degree']

                    self.natal_chart['houses'].append((house, sign, degree))
            
            elif key == 'ascendant' or key == 'vertex' or key == 'midheaven':
                self.natal_chart[key] = values
            
            elif key == 'lilith':
                full_degree = values['full_degree']
                norm_degree = values['norm_degree']
                speed = values['speed']
                is_retrograde = values['is_retro']
                sign = values['sign'].lower()
                house = values['house']

                self.natal_chart['lilith'] = (full_degree, norm_degree, speed, is_retrograde, sign, house)

            elif key == 'aspects':
                for value in values:
                    aspecting_planet = value['aspecting_planet'].lower()
                    aspected_planet = value['aspected_planet'].lower()
                    aspect = value['type'].lower()
                    orb = value['orb']
                    diff = value['diff']

                    self.natal_chart['aspects'].append((aspected_planet, aspecting_planet, aspect, orb, diff))

            elif key == 'moon_phase':
                moon_phase_name = values['moon_phase_name']
                self.natal_chart['moon_phase'].append(moon_phase_name)

            elif key == 'elements':
                for value in values['elements']:
                    name = value['name']
                    percentage = value['percentage']
                    self.natal_chart['elements'].append((name, percentage))

            elif key == 'modes':
                for value in values['modes']:
                    name = value['name']
                    percentage = value['percentage']
                    self.natal_chart['modes'].append((name, percentage))
            
            elif key == 'dominant_signs':
                sign = values['sign_name']
                percentage = values['percentage']


    ####################################################
    #    Private methods for creating the index
    ####################################################

    def _create_index_transits_daily(self) -> int:
        """Create index from transits daily."""
        
        index = 0
    
        ### Look at super bullish transits

        super_bullish_planets = self.collective_intel['super_bullish_planets']
        investing_houses = self.collective_intel['investing_houses']
        planets_exaltation = self.general_intel['planets_exaltation']

        for planet in super_bullish_planets:
            
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index += float(self.feature_ranking['exalted_planet'])
            
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= float(self.feature_ranking['retrograde_planet'])
            
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index += float(self.sentiment_ranking['super_bullish'])

        ### Look at bullish transits

        bullish_planets = self.collective_intel['bullish_planets']
        
        for planet in bullish_planets:
            
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index += float(self.feature_ranking['exalted_planet'])
            
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= float(self.feature_ranking['retrograde_planet'])
            
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index += float(self.sentiment_ranking['bullish'])

            # TODO: add angles in exaltation
            # TODO: add path of fortune in exaltation

        ### Look at bearish transits

        bearish_planets = self.collective_intel['super_bearish_planets']
        bearish_houses = self.collective_intel['other_houses']
        
        for planet in bearish_planets:
            
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index -= float(self.feature_ranking['detriment_planet'])
            
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= float(self.feature_ranking['retrograde_planet'])
            
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index -= float(self.sentiment_ranking['bearis_planet'])
            
            for house in bearish_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index -= float(self.sentiment_ranking['super_bearish'])

            # TODO: add angles in detriment

        ### Return the index
        return index


    def _create_index_transits_monthly(self) -> dict:
        """Create index from transits monthly."""
        angle_aspects_ranking = self.general_intel['angle_aspects_ranking']

        # create a new (temporal) sorted structure for dates vs. indexes
        # date and data has the following format:
        # '1-10-2023': [('moon', 'uranus', 'trine', 3.79), ('moon', 'neptune', 'sextile', 0.47)]
        for date, data in self.transit_monthly.items():
            
            self.transit_index[date] = 0

            for t in data:
                planet1, planet2, transit_type, orb = t
                if planet1 == planet2:
                    continue

                index_here = float(angle_aspects_ranking[transit_type]) * (10 - float(orb)) / 10
                self.transit_index[date] += index_here

    
    def _create_index_transits_daily_custom(self) -> dict:
        """Create index from custom transits daily."""

        for date, data in self.transit_now_custom.items():
            
            self.transit_index[date] = 0
            planets_exaltation = self.general_intel['planets_exaltation']
            planets_detriment = self.general_intel['planets_detriment']
            investing_houses = self.collective_intel['investing_houses']

            for t in data:
                planet1, planet2, transit_type, is_retrograde, sign, house = t
                if planet1 == planet2:
                    continue
                
                if is_retrograde:
                    self.transit_index[date] -= float(self.feature_ranking['retrograde_planet'])
                
                if sign in planets_exaltation[planet2]:
                    self.transit_index[date] += float(self.feature_ranking['exalted_planet'])
                    if house in investing_houses:
                        self.transit_index[date] += float(self.sentiment_ranking['super_bullish'])
                elif sign in planets_detriment[planet2]:
                    self.transit_index[date] -= float(self.feature_ranking['detriment_planet'])
                    if house in investing_houses:
                        self.transit_index[date] -= float(self.sentiment_ranking['super_bearish'])
                else:
                    if house in investing_houses:
                        self.transit_index[date] += float(self.sentiment_ranking['bullish'])
                    else:
                        self.transit_index[date] -= float(self.sentiment_ranking['bearish'])


    def _create_index_transits_moon(self) -> dict:
        """Create index from moon phase."""

        this_index = 0
        moon_phases_ranking = self.moon_intel['phase']

        for date, phase in self.moon_phase.items():
            this_ranking = moon_phases_ranking[phase]
            # TODO: fix this
            #this_index += float(self.ranking[this_ranking])

        if date in self.transit_index:
            self.transit_index[date] += this_index
        else:
            self.transit_index[date] = this_index

        return this_index


    def _create_index_transits_forecast(self) -> dict:
        """Create index from transit forecast."""

        this_index = 0
        super_bullish_planets = self.collective_intel['super_bullish_planets']
        investing_houses = self.collective_intel['investing_houses']
        planets_exaltation = self.general_intel['planets_exaltation']
    
        for planet, data in self.transit_forecast.items():
            full_degree, norm_degree, speed, is_retrograde, sign, house = data

            if planet in planets_exaltation:
                this_index += float(self.feature_ranking['exalted_planet'])
            
            if planet in self.retrogrades_now:
                this_index -= float(self.feature_ranking['retrograde_planet'])
            
            if house in investing_houses:
                this_index += float(self.sentiment_ranking['super_bullish'])
            
            if planet in super_bullish_planets:
                this_index += float(self.sentiment_ranking['super_bullish'])
            
        
        return this_index


    def _create_index_chart_data(self) -> dict:
        """Create index from chart data."""

        this_index = 0
        houses_ranking = self.collective_intel['investing_houses']
        aspects_ranking = self.general_intel['angle_aspects_ranking']

        for house in self.chart_data['houses']:
            start_degree, end_degree, sign, house, planets = house
            if house in houses_ranking:
                this_index += float(self.sentiment_ranking['super_bullish'])
        
        for aspect in self.chart_data['aspects']:
            aspected_planet, aspecting_planet, aspect, orb, diff = aspect
            # the api has a typo 'semi sqaure'
            if aspect in aspects_ranking:
                this_index += float(aspects_ranking[aspect])
            else:
                os.log_debug(f'Aspect {aspect} not found in aspects_ranking')

        return this_index


    def _create_index_whole_sign_houses(self) -> dict:
        """Create index from whole sign houses."""

        this_index = 0
        houses_ranking = self.collective_intel['investing_houses']
        aspects_ranking = self.general_intel['angle_aspects_ranking']

        for planet in self.whole_sign_houses['planets']:
            planet, full_degree, norm_degree, speed, is_retrograde, sign, house = planet
            if house in houses_ranking:
                this_index += float(self.sentiment_ranking['super_bullish'])
        
        for aspect in self.whole_sign_houses['aspects']:
            aspected_planet, aspecting_planet, aspect, orb, diff = aspect
            # the api has a typo 'semi sqaure'
            if aspect in aspects_ranking:
                this_index += float(aspects_ranking[aspect])
            else:
                os.log_debug(f'Aspect {aspect} not found in aspects_ranking')
        
        # TODO: deal with houses, midheaven, vertex, lilith

        return this_index


    def _create_index_natal_chart(self) -> dict:
        """Create index from natal chart."""

        this_index = 0
        houses_ranking = self.collective_intel['investing_houses']
        aspects_ranking = self.general_intel['angle_aspects_ranking']

        for planet in self.natal_chart['planets']:
            planet, full_degree, norm_degree, speed, is_retrograde, sign, house = planet
            if house in houses_ranking:
                this_index += float(self.sentiment_ranking['super_bullish'])
        
        for aspect in self.natal_chart['aspects']:
            aspected_planet, aspecting_planet, aspect, orb, diff = aspect
            # the api has a typo 'semi sqaure'
            if aspect in aspects_ranking:
                this_index += float(aspects_ranking[aspect])
            else:
                os.log_debug(f'Aspect {aspect} not found in aspects_ranking')


    #############################
    #       Public methods
    #############################

    def get_collective_forecast_today(self) -> None:
        """
            Get collective forecast now.

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

        os.log_info(f'Getting collective forecast today...')
        data = self._request_transits_daily()
        self._parse_data_transits_daily(data)
        
        this_index = self._create_index_transits_daily()
        key = net.get_date_from_timezone(self.timespace['tzone_name']).strftime("%Y-%m-%d_%H-%M-%S")

        self.collective_index[key] = this_index
        os.log_info(f'Daily Index ({key}): {this_index}')


    def get_collective_forecast_monthly(self) -> None:
        """
            Get collective forecast monthly.

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

        os.log_info(f'Getting collective forecast monthly...')
        data = self._request_transits_monthly()
        self._parse_data_transits_monthly(data)
        
        self._create_index_transits_monthly()
        os.log_info(f'Monthly indexes: {self.transit_index}')


    def get_collective_forecast_custom(self) -> None:
        """ 
            Get collective custom forecast daily.

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

        os.log_info(f'Getting collective custom forecast daily...')
        data = self._request_transits_custom_daily()
        
        self._parse_data_transits_daily_custom(data)
        
        self._create_index_transits_daily_custom()
        os.log_info(f'Daily custom indexes: {self.transit_index}')


    # TODO: move moon to other class?
    def get_collective_forecast_moon(self) -> None:
        """ 
            Get moon phase forecast.

            {
                "considered_date": "2-10-2017",
                "moon_phase": "Balsamic Moon",
                "significance": 
            }
        """

        # TODO: get other times
        os.log_info(f'Getting collective forecast moon...')
        data = self._request_transits_moon()
        
        self._parse_data_transits_moon(data)
        
        this_index = self._create_index_transits_moon()
        os.log_info(f'Moon phases: {self.moon_phase}')
        os.log_info(f'Moon index: {this_index}')

    
    def get_transit_forecast(self) -> None:
        """
            Get transit forecast.

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

        os.log_info(f'Getting transit forecast...')
        data = self._request_transits_forecast()

        self._parse_data_transits_forecast(data)

        this_index = self._create_index_transits_forecast()
        os.log_info(f'Transit index: {this_index}')
        

    def get_wheel(self) -> None:
        """Get wheel forecast."""

        os.log_info(f'Getting wheel...')
        data = self._request_wheel()

        self._parse_data_wheel(data)
    

    def get_chart_data(self) -> None:
        """
            Get chart data.
            This endpoint brings more aspects (e.g., quintile, semisextile).

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

        os.log_info(f'Getting chart data...')
        data = self._request_chart_data()

        self._parse_data_chart_data(data)

        this_index = self._create_index_chart_data()
        os.log_info(f'Chart data index: {this_index}')


    def get_whole_sign_houses(self) -> None:
        """
            Get whole sign houses.
            This endpoint brings vertex, midheaven, lilith
            and can be set to whole sign.

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

        os.log_info(f'Getting whole sign houses...')
        data = self._request_whole_sign_houses()

        self._parse_data_whole_sign_houses(data)

        this_index = self._create_index_whole_sign_houses()
        os.log_info(f'Whole sign houses index: {this_index}')


    def get_natal_chart(self) -> None:
        """
            Get natal chart.
            This endpoint brings vertex, midheaven, lilith,
            plus a lot of other data (element analysis, moon phase, etc.).
        """

        os.log_info(f'Getting natal chart...')
        data = self._request_natal_chart()

        self._parse_data_natal_chart(data)

        this_index = self._create_index_natal_chart()
        os.log_info(f'Natal chart index: {this_index}')