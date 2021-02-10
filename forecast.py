import requests, pandas, time
from datetime import datetime
from passwords import *

excl = "current,minutely,hourly,alerts"

openweather_api_call = "https://api.openweathermap.org/data/2.5/onecall?lat="+ lat + "&lon=" + \
				       lon + "&exclude=" + excl + "&appid=" + openweather_key + "&units=imperial"


def get_forecast():
	global high_tomorrow, low_tomorrow, sunrise_tomorrow, sunset_tomorrow
	weather_data = requests.get(openweather_api_call).json()
	temps_tomorrow = weather_data["daily"][1]["temp"]
	high_tomorrow = temps_tomorrow["max"]
	low_tomorrow = temps_tomorrow["min"]
	sunrise_tomorrow = weather_data["daily"][1]["sunrise"]
	sunset_tomorrow = weather_data["daily"][1]["sunset"]
	sunrise_tomorrow = datetime.fromtimestamp(sunrise_tomorrow).strftime('%H:%M')
	sunset_tomorrow = datetime.fromtimestamp(sunset_tomorrow).strftime('%H:%M')
