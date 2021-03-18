# uses the amadeus flight offers api to track prices of flights at specified intervals
# tracked daily, and stored in sqlite database for analysis

from amadeus import Client, ResponseError
import re
from datetime import date, timedelta
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
    
def new_flight(connection, sql, data):
    cursor = connection.cursor()
    try:
        cursor.execute(sql, data)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

# create database
connection = create_connection("price_flight_tracker.sqlite")
cursor = connection.cursor()
create_flights_table = """
CREATE TABLE IF NOT EXISTS flights (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  carrier TEXT,
  currency TEXT,
  departure_date TEXT,
  return_date TEXT,
  week INTEGER,
  weekday INTEGER,
  legs INTEGER,
  flights_found INTEGER,
  price FLOAT
);
"""
cursor.execute(create_flights_table)
connection.commit()

sql = """
INSERT INTO
  flights (carrier, currency, departure_date, return_date, week, weekday, legs, flights_found, price)
VALUES(?,?,?,?,?,?,?,?,?)
"""

today = date.today()
weekday = date.today().weekday()
for i in range(10):
	# perform 10 searches, with the departure date updated in two week increments
	# return flight is three weeks after departure
	start = today + timedelta(days=(14*(i+1)))
	end = start + timedelta(days=21)
	week = 2*(i+1)
	amadeus = Client(
		client_id='YOUR_AMADEUS_API_KEY',
    	client_secret='YOUR_AMADEUS_API_SECRET'
	)
	# roundtrip flights from Seattle to Budapest
	try:
		response = amadeus.shopping.flight_offers_search.get(
			originLocationCode='SEA',
			destinationLocationCode='BUD',
			departureDate=start,
			returnDate=end,
			currencyCode='USD',
			adults=1)
	
	except ResponseError as error:
		print(error)

	for flight in response.data:
		itinerary = str(flight['itineraries'])
		legs = itinerary.count('departure')
		# consider cheapest flight with less than 4 legs roundtrip
		if legs < 5 and flight['validatingAirlineCodes'][0] != 'DE' and flight['validatingAirlineCodes'][0] != 'QR':
			carrier = flight['validatingAirlineCodes'][0]
			currency = flight['price']['currency']
			departure_date = str(start)
			return_date = str(end)
			flights_found = len(response.data)
			price = flight['price']['total']
			data = (carrier, currency, departure_date, return_date, week, weekday, legs, flights_found, price)
			# add data to database
			new_flight(connection, sql, data)
			break


