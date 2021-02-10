import requests, mysql.connector, datetime, time
import pandas as pd
from passwords import *

#code to grab weather data from sensor
def get_weather():
	global weather, temp, humid, pressure
	#get weather data
	weather = requests.get("http://192.168.1.26:5000/").json()
	temp = round(weather["temp"],1)
	humid = round(weather["humid"],1)
	pressure = round(weather["pressure"],0)

# sets up database if it doesn't already exist
db = mysql.connector.connect(
    host = "localhost",
    user = dbuser,
    passwd = dbpassword,
    database = "weather"
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

#create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS weather;")
#cursor.execute("DROP TABLE weatherlog")
cursor.execute("CREATE TABLE IF NOT EXISTS weatherlog (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,time DATETIME, temperature float(5), humidity float(5),pressure float(5))")


# function to update tables
def grab_weather():

	#get current datetime
	now = datetime.datetime.now()

	#get values for insertion into table
	get_weather()
	values = (now, weather["temp"], weather["humid"], weather["pressure"])
	add_weather = ("INSERT INTO weatherlog (time, temperature, humidity, pressure) VALUES (%s, %s, %s, %s)")

	cursor.execute(add_weather, values)

	

# while True:
# 	grab_weather()
# 	time.sleep(30)

updatecount = 0

for i in range(1):
	updatecount += 1
	print(updatecount)
	grab_weather() 
	time.sleep(5)



#print table
gettable = "SELECT * FROM weatherlog"
# cursor.execute(gettable)
# fulltable = cursor.fetchall()
# print(fulltable)
tableresults = pd.read_sql_query(gettable, db)
print(tableresults)


# weatherquery = "SELECT * FROM weatherlog WHERE time IN (SELECT max(time) FROM weatherlog) "
# cursor.execute(weatherquery)
# weatherinfo = cursor.fetchall()
# print(weatherinfo)

# weatherdf = pd.read_sql_query(weatherquery, db)
# temp = weatherdf["temperature"].item()
# print(type(temp))

# print("temperature equals " + str(temp))
