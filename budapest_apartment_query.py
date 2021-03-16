# query Budapest apartments database

import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        #column_names = [description[0] for description in cursor.description]
        #print(column_names)
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        
        
connection = create_connection("budapest_apartments.sqlite")


# number of entries
select_apts = """
SELECT COUNT(*) from apartments
"""
num_apts = execute_read_query(connection, select_apts)[0][0]
print(f"There are {num_apts} apartments in the database.")
# originally 12695 entries in database


# number of unique entries
unique = """
SELECT COUNT(*)
FROM (SELECT DISTINCT address, size , price FROM apartments)
"""
uni = execute_read_query(connection, unique)[0][0]
print(f"There are {uni} apartments without duplicates in the database.")
# 9900 unique rows


# apartments with price changes
price_changes = """
SELECT 9900 - COUNT(*) 
FROM(SELECT DISTINCT address, size FROM unique_apartments)
"""
pc = execute_read_query(connection, price_changes)[0][0]
print(f"{pc} rows consist of price changes.")
# 1102 rows consist of price changes


# create a table without duplicate apartments
# populate = """
# CREATE TABLE unique_apartments AS
# SELECT DISTINCT address, size, price
# FROM apartments;
# """
# execute_read_query(connection, populate)
# contains 9900 entries


# delete empty table
# drop = """
# DROP TABLE uniq_apts;
# """
# execute_read_query(connection, drop)


# tables in database
# cursor = connection.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())


# second district apartments
dist_2 = """
SELECT COUNT(*) FROM unique_apartments
WHERE address LIKE '% II.%'
"""
dist_2_apts = execute_read_query(connection, dist_2)[0][0]
print(f"There are {dist_2_apts} apartments in the second district.")
# 571 apartments


# average price of second district apartments in certain size range
average_price = """
SELECT AVG(price)
FROM unique_apartments
WHERE address LIKE '% II.%'
AND 35 < size AND size < 42
"""
avg_price = execute_read_query(connection, average_price)[0][0]
print(f"Average price of 2nd dist. apts between 35 and 42 sqm is {avg_price:.2f}m HUF.")
# 34.87 million HUF

# median price
median_price = """
SELECT price
FROM unique_apartments
ORDER BY price
LIMIT 1
OFFSET (SELECT COUNT(*)
        FROM unique_apartments) / 2
"""
median_price = execute_read_query(connection, median_price)[0][0]
print(f"Median price of Budapest apartments is {median_price:.2f}m HUF.")
# 34.87 million HUF


# number of apartments at each size
# sizes = """
# SELECT COUNT(*), size
# FROM unique_apartments
# GROUP BY size
# """
# sizes = execute_read_query(connection,sizes)
# for size in sizes:
# 	print(size)


# q = """
# SELECT *
# FROM unique_apartments
# WHERE address LIKE '%Bem %'
# """
# apts = execute_read_query(connection, q)
# for apt in apts:
# 	print(apt)





