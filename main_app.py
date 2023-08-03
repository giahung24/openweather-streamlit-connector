import streamlit as st
import pandas as pd
from datetime import datetime
from connection import OpenWeatherConnection
import traceback 

st.set_page_config(page_title="OpenWeatherAPI Connection for Streamlit")
st.title("OpenWeatherAPI Connection for Streamlit")

st.info('A demo app with basic use of custom API connector built using ExperimentalBaseConnection. For more detail of OpenWeatherMap API, cf. [API doc](https://openweathermap.org/api)')

st.header("Setup")
"""`OpenWeatherConnection` gets your `api_key` (`appid`) from `./streamlit/secrets.toml` in the following format:"""
secrets = """
 [connections.openweathermap]
 OPEN_WEATHER_API_KEY = "your-key"
"""
st.code(secrets, language='toml')


st.header("Usage")

st.subheader(" Query")

"""
You can use the `query()` method to call any API with this template 'http://api.openweathermap.org/{api_name}/{version}/{endpoint}?{query}'. The `appid` is already added under the hood.

For example, to get the geographical coordinates (lat, lon) by using name of a location (eg. Paris), we can call the Geocoding API with the following template 

'http://api.openweathermap.org/{geo}/{1.0}/{direct}?{q=London&limit=1}'

With this template, the usage of `query()` method looks like this:
"""
code = """
from connection import OpenWeatherConnection
import streamlit as st

conn = st.experimental_connection("openweathermap", type=OpenWeatherConnection)
city_geo = conn.query(api_name="geo", version="1.0", endpoint="direct", query=f"q=London&limit=1")
"""
st.code(code, language='python')

conn = st.experimental_connection("openweathermap", type=OpenWeatherConnection)
city_geo = conn.query(api_name="geo", version="1.0", endpoint="direct", query=f"q=London&limit=1")

"""
The output of `query()` method is an namespace object converted from the API response. With this convenient, we can access the result information as an object with attributs instead of a dictionary.
For example, to use the result of the previous `query()` call, our code can be :
"""
code = '''
if city_geo:
    city_geo = city_geo[0]  # the Geocoding Direct API endpoint returns a list of result, so we get only the top match
st.info(f""" The geographical coordinates (lat, lon) of London is ({city_geo.lat},{city_geo.lon}).

FYI, the french version of London is '{city_geo.local_names.fr}'""")'''

st.code(code, language='python')

if city_geo:
    city_geo = city_geo[0]
st.info(f""" The geographical coordinates (lat, lon) of London is ({city_geo.lat},{city_geo.lon}).
        
FYI, the french version of London is '{city_geo.local_names.fr}'""")

st.subheader("One call")

"""  [OpenWeather One Call API 3.0](https://openweathermap.org/api/one-call-3) : Get essential weather data and aggregated historical weather data. 

OpenWeatherConnection has the get_one_call() method to help you easily access this API. For example, to get weather data of Paris, the code can be:
"""

code = """
from connection import OpenWeatherConnection
import streamlit as st

conn = st.experimental_connection("openweathermap", type=OpenWeatherConnection)
res = conn.get_one_call(city="Paris")

"""
st.code(code, language='python')


"""------------------"""

city = st.text_input("City name", max_chars=50, value="Paris")

if(st.button("Get weather info")) or city=='Paris':
    try:
        city_geo = conn.get_coords(city)
        if city_geo is None:
            st.error("City name not found, try again!")
        else:
            res = conn.get_one_call(lon=city_geo.lon, lat=city_geo.lat)
            alerts = res.alerts if hasattr(res, "alerts") else []
            current_temp = str(round(res.current.temp-273.15, 2)) + " °C"
            current_weather = res.current.weather[0] # 
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"### Current weather for {city} ({city_geo.country})") 
                st.metric("Temperature", current_temp)
            with col2:
                st.image(f"http://openweathermap.org/img/wn/{current_weather.icon}@2x.png",width=70)
                st.write(current_weather.description)

            map_df = pd.DataFrame.from_dict({'latitude':[city_geo.lat], 'longitude':[city_geo.lon]})
            st.map(map_df, zoom=11, size=0.1)
            
            if alerts:
                st.markdown("### :warning: Alerts")
                for alert in alerts:
                    start = datetime.fromtimestamp(alert.start)
                    end = datetime.fromtimestamp(alert.end)
                    st.markdown(f"#### {alert.event}")
                    message = f"""From {start} to {end}  
{alert.description}"""
                    st.warning(message)
    except:
        st.error("City name invalid, try again!")
        traceback.print_exc()
    


""" 
-------
Above is an example of how we can process the response from the One Call API. 
The code of this demo can be view at the Github repo.
"""