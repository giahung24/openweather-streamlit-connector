import requests
import json

import streamlit as st

from types import SimpleNamespace
from streamlit.connections import ExperimentalBaseConnection


class OpenWeatherConnection(ExperimentalBaseConnection):

    def _connect(self):
        self._api_url = 'http://api.openweathermap.org/{api_name}/{version}/{endpoint}?{query}&appid=' + self._secrets.OPEN_WEATHER_API_KEY

    def _call_api(self, url):
        res=requests.get(url)
        return json.loads(res.text, object_hook=lambda d: SimpleNamespace(**d))
    
    def query(self, api_name, version, endpoint, query, ttl=600):
        """ Call the OpenWeather API from this template 'http://api.openweathermap.org/{api_name}/{version}/{endpoint}?{query}' with 'appid' predefined

        Returns
        -------
        Object
            namedspace object of API response
        """
        @st.cache_data(ttl=ttl)
        def _get(api_name=api_name, version=version, endpoint=endpoint, query=query):
            url = self._api_url.format(api_name=api_name, version=version, 
                                   endpoint=endpoint, query=query)
            return self._call_api(url)
        return _get(api_name, version, endpoint, query)

    def get_coords(self, city, ttl=3600):
        """ Get geographical coordinates (lat, lon) by using name of the location (city name or area name)
        cf. https://openweathermap.org/api/geocoding-api

        Returns
        -------
        Object
            namedspace object of API response (only the first result in list)
        """
        res = self.query(api_name="geo", version="1.0", endpoint="direct", query=f"q={city}", ttl=ttl)
        if len(res) > 0:
            return res[0]

    def get_one_call(self, city, exclude=None, units=["metrics"], ttl=900):
        """ Get current weather, minute forecast for 1 hour, hourly forecast for 48 hours, daily forecast for 8 days and government weather alerts
        https://openweathermap.org/api/one-call-3#current
        """
        city_geo = self.get_coords(city)
        exclude_part = "" if exclude is None else "&exclude=" + ",".join(exclude)
        units =  ",".join(units)
        return self.query(api_name="data", version="3.0", endpoint="onecall", query=f"lat={city_geo.lat}&lon={city_geo.lon}{exclude_part}&units={units}", ttl=ttl)
