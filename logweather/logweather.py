import requests, mysql.connector, datetime, time
import pandas as pd
from passwords import *


# function to set up database
def load_weather_db():
	global db
	db = mysql.connector.connect(
    		host = "localhost",
    		user = dbuser,
    		passwd = dbpassword,
    		database = "weather")

#function to close weather db
def close_db():
	global cursor,db
	cursor.close()
	db.close()

#set up database if it doesn't already exist
load_weather_db()
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS weather;")
cursor.execute("CREATE TABLE IF NOT EXISTS weatherlog (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,time DATETIME, temperature float(5), humidity float(5),pressure float(5))")

close_db()

#cursor.close()
#db.close()

#code to grab weather data from sensor
def get_weather():
	global weather, temp, humid, pressure

	#get weather data
	weather = requests.get("http://192.168.1.26:5000/").json()
	temp = round(weather["temp"],1)
	humid = round(weather["humid"],1)
	pressure = round(weather["pressure"],0)



# function to update tables
def grab_weather():
	#get current datetime
	now = datetime.datetime.now()

	#get values for insertion into table
	get_weather()
	values = (now, weather["temp"], weather["humid"], weather["pressure"])

	#load database
	load_weather_db()
	cursor = db.cursor()

	add_weather = ("INSERT INTO weatherlog (time, temperature, humidity, pressure) VALUES (%s, %s, %s, %s)")
	cursor.execute(add_weather, values)
	close_db()




#grab and update weather every 2 minutes
while True:
	grab_weather()

	#load database
	load_weather_db()
	weatherquery = "SELECT * FROM weatherlog WHERE time IN (SELECT max(time) FROM weatherlog) "
	weatherdf = pd.read_sql_query(weatherquery, db)
	print(datetime.datetime.now().time())
	print(weatherdf)
	close_db()
	time.sleep(120)


#updatecount = 0
#for i in range(2):
#	updatecount += 1
#	print(updatecount)
#	grab_weather()
#	db.commit()
#	time.sleep(5)

#cursor.execute(weatherquery)
#weatherinfo = cursor.fetchall()
#print(weatherinfo)


#print table
#gettable = "SELECT * FROM weatherlog"
# cursor.execute(gettable)
# fulltable = cursor.fetchall()
# print(fulltable)
#print("full table:")
#tableresults = pd.read_sql_query(gettable, db)
#print(tableresults)

#print("Most recent:")
#weatherdf = pd.read_sql_query(weatherquery, db)
#temp = weatherdf["temperature"].item()

#print(weatherdf)
#print(temp)
#print(type(temp))

#print("temperature equals " + str(temp))
