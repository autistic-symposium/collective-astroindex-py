# -*- encoding: utf-8 -*-
# src/intel/collective.py


import src.utils.os as os
import src.utils.network as net
import src.datalake.astro_api_wrapper as aw


class CollectiveIndex:

    def __init__(self, city=None, country=None):

        ######################
        ### Load intel YAMLs
        ######################
        self.env_vars = os.load_config()
        self.ranking = self._load_ranking()
        self.api = aw.AstrologyAPIWrapper(self.env_vars)
        
        self.dignities_info = self._load_general_info('STRATEGIES_GENERAL', 'dignities')
        
        self.ascendant_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'ascendant')
        self.midheaven_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'midheaven')
        self.vertex_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'vertex')
        self.houses_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'houses')
        self.planet_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'planets')
        self.retrograde_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'retrograde')
        self.dignities_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'dignities')
        self.aspect_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'aspects')
        self.moon_phase_intel = self._load_intel('STRATEGIES_COLLECTIVE', 'moon_phase')

        ########################
        ### Create data dicts 
        ########################
        self.transit_daily = {t: [] for t in ['ascendant', 'date', 'houses', 'aspects']}
        self.transit_monthly = {t: [] for t in ['aspects', 'moon_phase']}
        self.transits_natal_daily = {t: [] for t in ['ascendant', 'date', 'aspects']}
        self.moon_phase = {t: [] for t in ['date', 'phase']}
        self.planet_tropical = {}
        self.chart_data = {t: [] for t in ['houses', 'aspects']}
        self.western_horoscope = {t: [] for t in ['planets', 'houses', 'aspects', 'ascendant_angle', 'midheaven_angle', 'vertex_angle']}

        self.collective_index = {}


    ################################
    #   Private methods: Set Up
    ################################

    def _load_ranking(self) -> None:

        try:
            ranking = os.load_yaml(self.env_vars['STRATEGIES_RANKING'])
            return {k: float(ranking['translation'][v]) for k, v in ranking['sentiments'].items()}
        except KeyError:
            os.exit_error(f'Error loading ranking file: {self.env_vars["STRATEGIES_RANKING"]}')

    def _translate_ranking(self, intel: dict) -> dict:

        return {k: float(self.ranking[v]) for k, v in intel.items()}

    def _load_intel(self, intel_file, key: str) -> None:

        intel = os.load_yaml(self.env_vars[intel_file])[key]
        return self._translate_ranking(intel)

    def _load_general_info(self, intel_file, key: str) -> None:

        return os.load_yaml(self.env_vars[intel_file])[key]


    ################################################
    #   Private methods: Parsing the response data
    ################################################

    def _parse_natal_wheel(self, data: dict) -> None:

        if 'status' in data and data['status'] == True:
            os.log_info(f'Chart created: {data["chart_url"]}')
        else:
            os.log_error(f'Error creating chart: {data["message"]}')
        

    def _parse_transits_daily(self, data: dict) -> None:

        self.transit_daily['ascendant'] = data['ascendant'].lower()
        self.transit_daily['date'] = os.convert_date_format(data['transit_date'])

        for feature in data['transit_house']:
            planet = feature['planet'].lower()
            sign = feature['natal_sign'].lower()
            house = feature['transit_house']
            is_retrograde = bool(feature['is_retrograde'])
            
            self.transit_daily['houses'].append({'planet': planet,
                                                'sign': sign,
                                                'house': house,
                                                'is_retrograde': is_retrograde})

        for aspect in data['transit_relation']:
            natal_planet = aspect['natal_planet'].lower()
            transit_planet = aspect['transit_planet'].lower()
            aspect_type = aspect['type'].lower()
            orb = float(aspect['orb'])
            
            self.transit_daily['aspects'].append({'natal_planet': natal_planet,
                                                  'transit_planet': transit_planet,
                                                  'aspect_type': aspect_type,
                                                  'orb': orb})  


    def _parse_transits_monthly(self, data: dict) -> None:

        self.transit_monthly['aspects'] = {}
        for aspect in data['transit_relation']:
            natal_planet = aspect['natal_planet'].lower()
            transit_planet = aspect['transit_planet'].lower()
            aspect_type = aspect['type'].lower()
            orb = float(aspect['orb'])
            date = os.convert_date_format(aspect['date'])

            self.transit_monthly['aspects'][date] = {
                                    'natal_planet': natal_planet,
                                    'transit_planet': transit_planet,
                                    'aspect_type': aspect_type,
                                    'orb': orb}

        self.transit_monthly['phase'] = {}
        for moon_phase in data['moon_phase']:
            phase = moon_phase['phase_type'].lower()
            date = os.convert_date_format(moon_phase['date'].split('T'))
            sign = moon_phase['sign'].lower()
            house = moon_phase['house']
            
            self.transit_monthly['phase'][date] = {
                                    'phase': phase,
                                    'sign': sign,
                                    'house': house}    


    def _parse_transits_natal_daily(self, data: dict) -> None:

        self.transits_natal_daily['ascendant'] = data['ascendant'].lower()
        self.transits_natal_daily['date'] = os.convert_date_format(data['transit_date'])

        for feature in data['transit_relation']:
            transit_planet = feature['transit_planet'].lower()
            natal_planet = feature['natal_planet'].lower()
            aspect_type = feature['aspect_type'].lower()
            is_retrograde = feature['is_retrograde']
            transit_sign = feature['transit_sign'].lower()
            natal_house = feature['natal_house']
            
            try:
                start_date = os.convert_date_format(feature['start_time'].split(' ')[0])
                end_date = os.convert_date_format(feature['end_time'].split(' ')[0])
            except KeyError:
                start_date = self.transits_natal_daily['date']
                end_date = self.transits_natal_daily['date']

            try:
                exact_date = os.convert_date_format(feature['exact_date'].split(' ')[0])
            except KeyError:
                exact_date = os.get_middle_datetime(start_date, end_date)

            self.transits_natal_daily['aspects'].append({'transit_planet': transit_planet,
                                                        'natal_planet': natal_planet,
                                                        'aspect_type': aspect_type,
                                                        'is_retrograde': is_retrograde,
                                                        'transit_sign': transit_sign,
                                                        'natal_house': natal_house,
                                                        'start_date': start_date,
                                                        'end_date': end_date,
                                                        'exact_date': exact_date})         


    def _parse_moon_phase(self, data: dict) -> None:

        self.moon_phase['date'] = os.convert_date_format(data['considered_date'])
        self.moon_phase['phase'] = data['moon_phase'].lower()


    def _parse_planet_tropical(self, data: dict) -> None:

        for item in data:
            planet = item['name'].lower()
            full_degree = item['fullDegree']
            norm_degree = item['normDegree']
            speed = item['speed']
            is_retrograde = item['isRetro']
            sign = item['sign'].lower()
            house = item['house']
            
            self.planet_tropical[planet] = {
                                    'full_degree': full_degree,
                                    'norm_degree': norm_degree,
                                    'speed': speed,
                                    'is_retrograde': is_retrograde,
                                    'sign': sign,
                                    'house': house}


    def _parse_chart_data(self, data: dict) -> None:

        for item in data['houses']:
            start_degree = item['start_degree']
            end_degree = item['end_degree']
            sign = item['sign'].lower()
            house = item['house_id']
            planets = item['planets']

            self.chart_data['houses'].append({'start_degree': start_degree, 
                                              'end_degree': end_degree,
                                              'sign': sign,
                                              'house': house,
                                              'planets': planets})

        for item in data['aspects']:
            natal_planet = item['aspected_planet'].lower()
            transit_planet = item['aspecting_planet'].lower()
            aspect_type = item['type'].lower()
            orb = item['orb']
            diff = item['diff']

            self.chart_data['aspects'].append({'natal_planet': natal_planet,
                                               'transit_planet': transit_planet,
                                               'aspect_type': aspect_type,
                                               'orb': orb,
                                               'diff': diff})   


    def _parse_western_horoscope(self, data: dict) -> None:

        self.western_horoscope['ascendan_angle'] = data['ascendant']
        self.western_horoscope['midheaven_angle'] = data['midheaven']
        self.western_horoscope['vertex_angle'] = data['vertex']
        self.western_horoscope['planets'] = { 'lilith': {
                                    'full_degree': data['lilith']['full_degree'],
                                    'norm_degree': data['lilith']['norm_degree'],
                                    'speed': data['lilith']['speed'],
                                    'is_retrograde': data['lilith']['is_retro'],
                                    'sign': data['lilith']['sign'].lower(),
                                    'house': data['lilith']['house']}
                                }

        for item in data['planets']:
            self.western_horoscope['planets'][item['name'].lower()] = {
                'full_degree': item['full_degree'],
                'norm_degree': item['norm_degree'],
                'speed': item['speed'],
                'is_retrograde': item['is_retro'],
                'sign': item['sign'].lower(),
                'house': item['house']}

        for item in data['houses']:
            self.western_horoscope['houses'].append({'house': item['house'],
                                                     'sign': item['sign'].lower(),
                                                     'degree': item['degree']})

        for item in data['aspects']:
            self.western_horoscope['aspects'].append({'natal_planet': item['aspected_planet'].lower(),
                                                      'transit_planet': item['aspecting_planet'].lower(),
                                                      'aspect_type': item['type'].lower(),
                                                      'orb': item['orb'],
                                                      'diff': item['diff']})
            

        
    #############################################
    #    Private methods: Intel for indexes
    #############################################

    def _calculate_intel_for_ascendant(self, ascendant) -> int:

        if ascendant in self.ascendant_intel:
            return self.ascendant_intel[ascendant]
        else:
            return 0
    

    def _calculate_intel_for_midheaven(self, midheaven) -> int:
            
            if midheaven in self.ascendant_intel:
                return self.midheaven_intel[midheaven]
            else:
                return 0

    def _calculate_index_for_vertex(self, vertex) -> int:

        if vertex in self.ascendant_intel:
            return self.vertex_intel[vertex]
        else:
            return 0


    def _calculate_intel_for_retrograde(self, is_retrograde) -> int:

        if is_retrograde is not None:
            return self.retrograde_intel[bool(is_retrograde)]
        else:
            return 0
        

    def _calculate_intel_for_sign(self, sign, planet) -> int:
        
        try:
            if sign in self.dignities_info[planet]:
                try:
                    return abs(self.dignities_intel[self.dignities_info[planet][sign]])
                except KeyError:
                    os.log_debug(f'Error: {sign} not found in dignities_intel')
        except KeyError:
            os.log_debug(f'Error: {planet} not found in dignities_info')

        return 0


    def _calculate_intel_for_house(self, house) -> int:

        if house in self.houses_intel:
            return self.houses_intel[house]
        else:
            return 0


    def _calculate_intel_for_planet(self, planet) -> int:

        if planet in self.planet_intel:
            return abs(self.planet_intel[planet])
        else:
            return 0


    def _calculate_intel_for_aspect(self, aspect) -> int:

        if aspect in self.aspect_intel:
            return self.aspect_intel[aspect]
        else:
            return 0


    def _calculate_intel_for_orb(self, orb) -> int:

        if orb is None:
            return 2
        else:
            return 1 - (orb / 10)


    #################################################
    #    Private methods: Assembly intel for indexes
    #################################################

    def _calculate_index_for_ascendant(self, ascendant) -> int:

        return self._calculate_intel_for_ascendant(ascendant)

    
    def _calculate_index_for_midheaven(self, midheaven) -> int:

        return self._calculate_intel_for_midheaven(midheaven)

    
    def _calculate_index_for_vertex(self, vertex) -> int:

        return self._calculate_intel_for_vertex(vertex)
    

    def _calculate_index_for_houses_by_planet(self, houses) -> int:

        index = 0

        for item in houses:
            house = item['house'] 
            planet = item['planet'] 
            sign = item['sign'] 
            is_retrograde = item['is_retrograde']
            
            retrograde_index = self._calculate_intel_for_retrograde(is_retrograde)
            planet_index = self._calculate_intel_for_planet(planet)
            house_index = self._calculate_intel_for_house(house)
            sign_index = self._calculate_intel_for_sign(sign, planet)
            
            index += planet_index * (retrograde_index + sign_index + house_index)
            
        return index

    
    def _calculate_index_for_houses_by_planets(self, houses) -> int:
            
            index = 0
    
            for item in houses:
                house = item['house'] 
                planets = item['planets'] 
                start_degree = item['start_degree']
                end_degree = item['end_degree']
                
                for item in planets:
                    planet = item['name'].lower()
                    sign = item['sign'].lower()
                    is_retrograde = item['is_retro']
                    full_degree = item['full_degree']
                    
                    planet_index = self._calculate_intel_for_planet(planet)
                    sign_index = self._calculate_intel_for_sign(sign, planet)
                    retrograde_index = self._calculate_intel_for_retrograde(is_retrograde)
                    
                    index += planet_index * (retrograde_index + sign_index)
                
                index += self._calculate_intel_for_house(house)
                    
            return index


    def _calculate_index_for_aspect(self, aspect) -> int:

        transit_planet = aspect['transit_planet']
        natal_planet = aspect['natal_planet']
        aspect_type = aspect['aspect_type']
        orb = aspect['orb'] if 'orb' in aspect else None
        is_retrograde = aspect['is_retrograde'] if 'is_retrograde' in aspect else None
        transit_sign = aspect['transit_sign'] if 'transit_sign' in aspect else None
        house = aspect['house'] if 'house' in aspect else None
        
        transit_planet_index = self._calculate_intel_for_planet(transit_planet)
        natal_planet_index = self._calculate_intel_for_planet(natal_planet)
        aspect_index = self._calculate_intel_for_aspect(aspect_type)
        orb_index = self._calculate_intel_for_orb(orb)
        retrograde_index = self._calculate_intel_for_retrograde(is_retrograde)
        sign_index = self._calculate_intel_for_sign(transit_sign, transit_planet)
        house_index = self._calculate_intel_for_house(house)

        return (transit_planet_index + natal_planet_index + aspect_index + house_index +
                                            retrograde_index + sign_index) * orb_index


    def _calculate_index_for_moon_phase(self, phase) -> int:

        phase_type = phase['phase']    
        sign = phase['sign'] if 'sign' in phase else None
        house = phase['house'] if 'house' in phase else None    
        
        phase_index = self.moon_phase_intel[phase_type] 
        planet_index = self._calculate_intel_for_planet('moon')
        house_index = self._calculate_intel_for_house(house)
        sign_index = self._calculate_intel_for_sign(sign, 'moon')

        return phase_index * (planet_index + house_index + sign_index)
        
    
    #############################################
    #    Private methods: Creating the indexes
    #############################################

    def _create_index_transits_daily(self) -> int:

        ascendant = self.transit_daily['ascendant']
        aspects = self.transit_daily['aspects']
        houses = self.transit_daily['houses']
        date = self.transit_daily['date']

        index_here = 0
        for aspect in aspects:

            index_here += self._calculate_index_for_aspect(aspect)

        index_here += self._calculate_index_for_ascendant(ascendant) + \
                                     self._calculate_index_for_houses_by_planet(houses) 

        if date in self.collective_index:
            self.collective_index[date] += index_here
        else:
            self.collective_index[date] = index_here

        return index_here
                                

    def _create_index_transits_monthly(self) -> None:

        aspects = self.transit_monthly['aspects']
        phase = self.transit_monthly['phase']

        for date, aspect in aspects.items():
            index_aspect = self._calculate_index_for_aspect(aspect)
            if date in self.collective_index:
                self.collective_index[date] += index_aspect
            else:
                self.collective_index[date] = index_aspect

        for date, phase in phase.items():
            index_phase = self._calculate_index_for_moon_phase(phase)
            if date in self.collective_index:
                self.collective_index[date] += index_phase
            else:
                self.collective_index[date] = index_phase

    
    def _create_transits_natal_daily(self) -> int:  

        ascendant = self.transits_natal_daily['ascendant']
        aspects = self.transits_natal_daily['aspects']
        date = self.transits_natal_daily['date']

        index_here = 0
        for aspect in aspects:
            index_here += self._calculate_index_for_aspect(aspect)

        index_here += self._calculate_index_for_ascendant(ascendant)

        if date in self.collective_index:
            self.collective_index[date] += index_here
        else:
            self.collective_index[date] = index_here

        return index_here


    def _create_index_moon_phase(self) -> dict:
        
        phase = self.moon_phase
        date = phase['date']
        index_here = self._calculate_index_for_moon_phase(phase)

        if date in self.collective_index:
            self.collective_index[date] += index_here
        else:
            self.collective_index[date] = index_here

        return index_here


    def _create_index_planet_tropical(self) -> dict:
        
        planets = self.planet_tropical
        index_here = 0

        for planet, data in planets.items():
            full_degree, norm_degree, speed, is_retrograde, sign, house = data
            index_here += self._calculate_intel_for_planet(planet)
            index_here += self._calculate_intel_for_sign(sign, planet)
            index_here += self._calculate_intel_for_house(house)
            index_here += self._calculate_intel_for_retrograde(is_retrograde)

        self.collective_index[self.api.get_request_date()] = index_here

        return index_here


    def _create_index_chart_data(self) -> dict:

        houses = self.chart_data['houses']
        aspects = self.chart_data['aspects']

        index_here = self._calculate_index_for_houses_by_planets(houses)

        for aspect in aspects:
            index_here += self._calculate_index_for_aspect(aspect)

        self.collective_index[self.api.get_request_date()] = index_here

        return index_here


    def _create_index_western_horoscope(self) -> dict:
        
        planets = self.western_horoscope['planets']
        houses = self.western_horoscope['houses']
        aspects = self.western_horoscope['aspects']
        ascendant_angle = self.western_horoscope['ascendant_angle']
        midheaven_angle = self.western_horoscope['midheaven_angle']
        vertex_angle = self.western_horoscope['vertex_angle']

        index_here = 0

        for planet, data in planets.items():
            index_here += self._calculate_intel_for_planet(planet)
            index_here += self._calculate_intel_for_sign(data['sign'], planet)
            index_here += self._calculate_intel_for_house(data['house'])
            index_here += self._calculate_intel_for_retrograde(data['is_retrograde'])

        for house in houses:
            index_here += self._calculate_intel_for_house(house['house'])
            index_here += self._calculate_intel_for_sign(house['sign'], 'ascendant')

        for aspect in aspects:
            index_here += self._calculate_index_for_aspect(aspect)

        self.collective_index[self.api.get_request_date()] = index_here

        return index_here


    #############################
    #       Public methods
    #############################

    def get_natal_wheel(self) -> None:

        response = self.api.request_natal_wheel()
        self._parse_natal_wheel(response)


    def get_transits_daily(self) -> None:

        response = self.api.request_transits_daily()
        self._parse_transits_daily(response)

        this_index = self._create_index_transits_daily()
        os.log_info(f'Index I.a: {this_index}')


    def get_transits_monthly(self) -> None:

        response = self.api.request_transits_monthly()
        self._parse_transits_monthly(response)

        self._create_index_transits_monthly()
        os.log_info(f'Index I.b: {self.collective_index}')


    def get_transits_natal_daily(self) -> None:

        response = self.api.request_transits_natal_daily()
        self._parse_transits_natal_daily(response)

        this_index = self._create_transits_natal_daily()
        os.log_info(f'Index I.c: {this_index}')


    def get_moon_phase(self) -> None:

        response = self.api.request_moon_phase()
        self._parse_moon_phase(response)
        
        this_index = self._create_index_moon_phase()

        os.log_info(f'Index I.d: {this_index}')

    
    def get_planet_tropical(self) -> None:

        response = self.api.request_planet_tropical()
        self._parse_planet_tropical(response)

        this_index = self._create_index_planet_tropical()

        os.log_info(f'Index I.e: {this_index}')
        

    def get_chart_data(self) -> None:

        response = self.api.request_chart_data()
        self._parse_chart_data(response)

        this_index = self._create_index_chart_data()

        os.log_info(f'Index I.f: {this_index}')


    def get_western_horoscope(self) -> None:
       
        response = self.api.request_western_horoscope()
        self._parse_western_horoscope(response)

        this_index = self._create_index_western_horoscope()

        os.log_info(f'Index I.g: {this_index}')


    def get_collective_index(self) -> None:

        self.get_transits_daily()
        self.get_transits_monthly()
        self.get_transits_natal_daily()
        self.get_moon_phase()
        self.get_planet_tropical()
        self.get_chart_data()
        self.get_western_horoscope()

        os.log_info(f'Collective index: {self.collective_index}')
