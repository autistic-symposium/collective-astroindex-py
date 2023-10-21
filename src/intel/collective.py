# -*- encoding: utf-8 -*-
# src/intel/collective.py

import src.utils.os as os
import src.utils.net as net


class Collective:

    def __init__(self, env_vars, city=None, country=None):
        self.env_vars = env_vars
        self.collective_index = 0
        self.location = (city, country)
        self.timespace = net.get_timespace_dict(self.location)
        self.ascendant_now = None
        self.houses_now = {h: [] for h in range(1, 13)}
        self.planets_now = {}
        self.retrogrades_now = []
        self.transit_now = {t: [] for t in ['conjunction', 'trine', 'square', 'opposition', 'sextile']}


    #############################
    #       Private methods
    #############################
    def _request_transits_daily(self) -> dict:
        """Request transits daily from API."""

        endpoint = 'tropical_transits/daily'
        return net.craft_request(self.env_vars, endpoint, self.timespace)
        

    def _parse_data_transits_daily(self, astro_data: dict) -> int:
        """Parse data from transits daily."""

        ### Divide and save the data
        self.ascendant_now = astro_data['ascendant'].lower()
        transit_house = astro_data['transit_house']
        transit_relation = astro_data['transit_relation']

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
            orb = t['orb']
            transit_type = t['type'].lower()

            if planet1 == planet2:
                continue
            
            self.transit_now[transit_type].append((planet1, planet2, orb))


    def _create_index_transits_daily(self) -> int:
        """Create index from transits daily."""
        
        index = 0
        intel = os.load_yaml(self.env_vars['STRATEGIES_GENERAL'])

        ##################################
        ### Look at super bullish transits
        ##################################
        super_bullish_planets = intel['super_bullish_planets']
        investing_houses = intel['investing_houses']
        planets_exaltation = intel['planets_exaltation']

        for planet in super_bullish_planets:
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index += 5
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= 3
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index += 10
        
        ##################################
        ### Look at bullish transits
        ##################################
        bullish_planets = intel['bullish_planets']
        for planet in bullish_planets:
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index += 1
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= 1
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index += 5

        ##################################
        ### Look at bearish transits
        ##################################
        bearish_planets = intel['super_bearish_planets']
        bearish_houses = intel['other_houses']
        for planet in bearish_planets:
            if self.planets_now[planet] in planets_exaltation:
                os.log_debug(f'{planet} is exalted in {self.planets_now[planet]}')
                index -= 2
            if planet in self.retrogrades_now:
                os.log_debug(f'{planet} is retrograde')
                index -= 1
            for house in investing_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index -= 5
            for house in bearish_houses:
                if planet in self.houses_now[house]:
                    os.log_debug(f'{planet} is in house {house}')
                    index -= 2


        return index

    #############################
    #       Public methods
    #############################

    def get_collective_forecast_now(self) -> None:
        """Get collective forecast now."""

        astro_data = self._request_transits_daily()
        self._parse_data_transits_daily(astro_data)
        this_index = self._create_index_transits_daily()
        os.log_debug(f'Collective index updated to: {this_index}')
        self.collective_index += this_index
