# -*- encoding: utf-8 -*-
# src/intel/collective.py

import src.utils.os as os
import src.utils.net as net


class Collective:

    def __init__(self, env_vars, city=None, country=None):
        self.env_vars = env_vars
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
        self.transit_monthly_index = {}

        self.ranking = self._get_ranking_scale()

        self.collective_intel = os.load_yaml(self.env_vars['STRATEGIES_COLLECTIVE'])
        self.general_intel = os.load_yaml(self.env_vars['STRATEGIES_GENERAL'])


    #############################
    #       Private methods
    #############################
    def _get_ranking_scale(self) -> dict:
        """Get ranking scale."""
    
        return os.load_yaml(self.env_vars['STRATEGIES_RANKING'])
        

    def _request_transits_daily(self) -> dict:
        """Request transits daily from API."""

        endpoint = 'tropical_transits/daily'
        return net.craft_request(self.env_vars, endpoint, self.timespace)


    def _request_transits_monthly(self) -> dict:
        """Request transits monthly from API."""

        endpoint = 'tropical_transits/monthly'
        return net.craft_request(self.env_vars, endpoint, self.timespace)
        

    def _parse_data_transits_daily(self, data: dict) -> int:
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


    def _parse_data_transits_monthly(self, data: dict) -> int:
        """Parse data from transits monthly."""

        ### Divide and save the data
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
        os.log_info(f'Moon phases: {self.moon_phase}')
        os.log_info(f'Transits monthly: {self.transit_monthly}')

        # TODO: why I am getting old dates? remove them

    
    def _create_index_transits_monthly(self) -> dict:
        """Create index from transits monthly."""
        angle_aspects_ranking = self.general_intel['angle_aspects_ranking']

        # create a new (temporal) sorted structure for dates vs. indexes
        # date and data has the following format:
        # '1-10-2023': [('moon', 'uranus', 'trine', 3.79), ('moon', 'neptune', 'sextile', 0.47)]
        for date, data in self.transit_monthly.items():
            
            self.transit_monthly_index[date] = 0

            for t in data:
                planet1, planet2, transit_type, orb = t
                if planet1 == planet2:
                    continue

                index_here = float(angle_aspects_ranking[transit_type]) * (10 - float(orb)) / 10
                self.transit_monthly_index[date] += index_here


    def _create_index_transits_daily(self) -> int:
        """Create index from transits daily."""
        
        index = 0
    
        ##################################
        ### Look at super bullish transits
        ##################################

        super_bullish_planets = self.collective_intel['super_bullish_planets']
        investing_houses = self.collective_intel['investing_houses']
        planets_exaltation = self.general_intel['planets_exaltation']

        for planet in super_bullish_planets:
            
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index += float(self.ranking['exalted'])
            
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= float(self.ranking['retrograde'])
            
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index += float(self.ranking['super_bullish'])

        
        ##################################
        ### Look at bullish transits
        ##################################

        bullish_planets = self.collective_intel['bullish_planets']
        
        for planet in bullish_planets:
            
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index += float(self.ranking['exalted'])
            
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= float(self.ranking['retrograde'])
            
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index += float(self.ranking['bullish'])

            # TODO: add angles in exaltation
            # TODO: add path of fortune in exaltation


        ##################################
        ### Look at bearish transits
        ##################################
        bearish_planets = self.collective_intel['super_bearish_planets']
        bearish_houses = self.collective_intel['other_houses']
        
        for planet in bearish_planets:
            
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index -= float(self.ranking['detriment'])
            
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= float(self.ranking['retrograde'])
            
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index -= float(self.ranking['bearish'])
            
            for house in bearish_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index -= float(self.ranking['super_bearish'])

            # TODO: add angles in detriment


        ##################################
        ### Return the index
        ##################################
        return index

    #############################
    #       Public methods
    #############################

    def get_collective_forecast_today(self) -> None:
        """Get collective forecast now."""

        os.log_info(f'Getting collective forecast today...')
        data = self._request_transits_daily()
        self._parse_data_transits_daily(data)
        
        this_index = self._create_index_transits_daily()
        key = net.get_date_from_timezone(self.timespace['tzone_name']).strftime("%Y-%m-%d_%H-%M-%S")

        self.collective_index[key] = this_index
        os.log_info(f'Current Index ({key}): {this_index}')


    def get_collective_forecast_monthly(self) -> None:
        """Get collective forecast monthly."""

        os.log_info(f'Getting collective forecast monthly...')
        data = self._request_transits_monthly()
        self._parse_data_transits_monthly(data)
        
        self._create_index_transits_monthly()
        os.log_debug(f'Monthly indexes: {self.transit_monthly_index}')
