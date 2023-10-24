# -*- encoding: utf-8 -*-
# src/datalake/AstrologyAPIWrapper.py

import src.utils.net as net
import src.utils.os as os


class AstrologyAPIWrapper:


    def get_timespace_dict(self, day=None, 
                                 month=None, 
                                 year=None, 
                                 hour=None, 
                                 mins=None, 
                                 lat=None, 
                                 lon=None, 
                                 tzone=None, 
                                 city=None, 
                                 country=None) -> dict:
        """Craft data to send to the API."""

        if not lat or not lon:
            lat, lon = net.get_lat_and_lon_at_given_city(city, country)
        os.log_debug(f'Using coordinates {lat}, {lon}')

        if not tzone:
            tzone_name, tzone = net.get_timezone_offset_at_given_location(lat, lon)
            os.log_debug(f'Using timezone {tzone}')

        if not day or not month or not year or not hour or not mins:
            day, month, year, hour, mins = net.get_datetime_now_at_given_timezone(tzone_name)
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



    def _request_transits_daily(self) -> dict:
        """Request transits daily from API."""

        endpoint = 'tropical_transits/daily'
        return net.craft_request(self.env_vars, endpoint, self.timespace)


    def _request_transits_monthly(self) -> dict:
        """Request transits monthly from API."""

        endpoint = 'tropical_transits/monthly'
        return net.craft_request(self.env_vars, endpoint, self.timespace)


    def _request_transits_custom_daily(self) -> dict:
        """Request custom transits daily from API."""

        endpoint = 'natal_transits/daily'
        return net.craft_request(self.env_vars, endpoint, self.timespace)


    def  _request_transits_moon(self) -> dict:
        """Request moon phase from API."""

        endpoint = 'moon_phase_report'
        return net.craft_request(self.env_vars, endpoint, self.timespace)

    
    def _request_transits_forecast(self) -> dict:
        """Request transits forecast from API."""

        endpoint = 'planets/tropical'
        return net.craft_request(self.env_vars, endpoint, self.timespace)

    
    def _request_wheel(self) -> dict:
        """Request wheel from API."""

        endpoint = 'natal_wheel_chart'
        custom_data = {
            'planet_icon_color': '#F57C00',
            'inner_circle_background': '#FFF8E1',
            'sign_icon_color': 'red',
            'sign_background': '#ffffff',
            'chart_size': '500',
            'image_type': 'png',
        }
        return net.craft_request(self.env_vars, endpoint, self.timespace, custom_data)


    def _request_chart_data(self) -> dict:
        """Request chart data from API."""

        endpoint = 'western_chart_data'
        return net.craft_request(self.env_vars, endpoint, self.timespace)

    
    def _request_whole_sign_houses(self) -> dict:
        """Request whole sign houses from API."""

        endpoint = 'western_horoscope'
        # TODO: which one is the one?
        custom_data = {
            'system': 'whole_sign',
            'house_system': 'whole_sign',
        }
        return net.craft_request(self.env_vars, endpoint, self.timespace, custom_data)

    def _request_natal_chart(self) -> dict:
        """Request natal chart from API."""

        endpoint = 'natal_chart_interpretation'
        return net.craft_request(self.env_vars, endpoint, self.timespace)

