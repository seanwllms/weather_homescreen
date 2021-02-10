import requests
from passwords import *

api_call_url = "https://api.enphaseenergy.com/api/v2/systems/" + \
                sysid + "/summary?key=" + solar_apikey + "&user_id=" + \
                user_id


def get_solar():
	global solarinfo, currentpower, energytoday, energylifetime
	solarinfo = requests.get(api_call_url).json()
	currentpower = str(solarinfo["current_power"]/1000)
	energytoday = str(solarinfo["energy_today"]/1000)
	energylifetime = str(solarinfo["energy_lifetime"]/1000)