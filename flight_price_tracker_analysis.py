# analyze flight price tracker database

import sqlite3
from sqlite3 import Error
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        
        
connection = create_connection("price_flight_tracker.sqlite")


# number of entries
count = """
SELECT COUNT(*) from flights;
"""
num_entries = execute_read_query(connection, count)[0][0]
print(f"\nThere are {num_entries} flights in the database.")


# number of unique airlines
unique = """
SELECT COUNT(*)
FROM (SELECT DISTINCT carrier FROM flights);
"""
uni = execute_read_query(connection, unique)[0][0]
print(f"There are {uni} carriers in the database.\n")


# last ten flights
last_ten = """
SELECT * FROM (
SELECT * FROM flights ORDER BY id DESC LIMIT 10)
ORDER BY id ASC;
"""
cursor = connection.cursor()
cursor.execute(last_ten)
result = cursor.fetchall()
column_names_list = [description[0] for description in cursor.description]
column_names = ""
for s in column_names_list:
	column_names += (s + " ")
print("The last ten flights:")
print(column_names)
for flight in result:
	print(flight)
print("")


# average price for day of week
for i in range(7):
	day = f"""
	SELECT AVG(price)
	FROM flights
	WHERE weekday = {i};
	"""
	avg_price = execute_read_query(connection, day)[0][0]
	print(f"Day of the week: {i}, average price = ${avg_price:.2f}")
print("(0 is Monday, 6 Sunday)\n")


# average price based on week from purchase
week, p = [], []
for i in range(2,21,2):
	day = f"""
	SELECT AVG(price)
	FROM flights
	WHERE week = {i};
	"""
	avg_price = execute_read_query(connection, day)[0][0]
	print(f"Week from purchase: {i}, average price = ${avg_price:.2f}")
	week.append(i)
	p.append(avg_price)
print("")
# plt.plot(week,p,marker='o')
# plt.ylim([500, 2500])
# plt.xticks(np.arange(2, 22, step=2))
# plt.xlabel("weeks from search")
# plt.ylabel("average price")
# plt.show()


# plot historical prices
historical = """
SELECT departure_date, price from flights
WHERE week = 6;
"""
historical_prices = execute_read_query(connection, historical)
dates = []
prices = []
for search in historical_prices:
	departure = datetime.strptime(search[0], "%Y-%m-%d").date() # '2021-04-29'
	day_searched = departure - timedelta(days=(42))
	dates.append(day_searched)
	prices.append(search[1])

plt.plot(dates,prices,marker='o')
plt.title("historical prices, six weeks out")
plt.ylim([700, 2000])
plt.gcf().autofmt_xdate()
plt.xlabel("date of search")
plt.ylabel("price")
plt.show()

