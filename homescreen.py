from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
import requests, mysql.connector
import pandas as pd
from passwords import *

#####################################################
############### SOLAR API QUERY CODE  ###############
#####################################################

api_call_url = "https://api.enphaseenergy.com/api/v2/systems/" + \
                sysid + "/summary?key=" + solar_apikey + "&user_id=" + \
                user_id

def get_solar():
	global solarinfo, currentpower, energytoday, energylifetime
	solarinfo = requests.get(api_call_url).json()
	currentpower = str(solarinfo["current_power"]/1000)
	energytoday = str(solarinfo["energy_today"]/1000)
	energylifetime = str(solarinfo["energy_lifetime"]/1000)


#####################################################
############### WEATHER DB QUERY CODE ###############
#####################################################
current_weather_query = "SELECT * FROM weatherlog WHERE time IN (SELECT max(time) FROM weatherlog)"

#connect to the database
db = mysql.connector.connect(
  		host = "localhost",
    		user = dbuser,
    		passwd = dbpassword,
  		database = "weather",
		autocommit=True
)


def get_weather():
	global weather, temp, humid, pressure, current_weather, db

	current_weather = pd.read_sql_query(current_weather_query, db)
	temp = current_weather["temperature"].item()
	humid = current_weather["humidity"].item()
	pressure = current_weather["pressure"].item()


#####################################################
############# FORECAST API QUERY CODE  ##############
#####################################################
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

#####################################################
############# ACTUAL FLASK APP CODE HERE ############
#####################################################
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def homescreen():
	get_weather()
	get_solar()
	get_forecast()
	return render_template("homescreen.html",
    	humidity = humid,
    	temperature = temp,
    	pressure = pressure, 
    	energylifetime = energylifetime,
    	energytoday = energytoday, 
    	currentpower = currentpower,
    	forecast_sunrise = sunrise_tomorrow,
    	forecast_sunset = sunset_tomorrow,
    	high_tomorrow = high_tomorrow,
    	low_tomorrow = low_tomorrow)
