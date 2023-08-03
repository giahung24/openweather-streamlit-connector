# OpenWeatherMap Connector for Streamlit
Simple OpenWeatherMap-Streamlit API wrapper. Built using ExperimentalBaseConnection.

## Usage example
```python
import streamlit as st
from connection import OpenWeatherConnection

conn = st.experimental_connection("openweathermap", type=OpenWeatherConnection)
city_geo = conn.query(api_name="geo", version="1.0", endpoint="direct", query=f"q=London&limit=1")
st.info(f""" The geographical coordinates (lat, lon) of London is ({city_geo.lat},{city_geo.lon}).
```

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://openweather-connector.streamlit.app/)