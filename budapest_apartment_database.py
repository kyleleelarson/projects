# create sqlite database of Budapest apartments listed on ingatlan.com

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
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
    
def new_apartment(connection, sql, data):
    cursor = connection.cursor()
    try:
        cursor.execute(sql, data)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

# create database
connection = create_connection("budapest_apartments.sqlite")
cursor = connection.cursor()
create_apartments_table = """
CREATE TABLE IF NOT EXISTS apartments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT NOT NULL,
  size INTEGER,
  price FLOAT
);
"""
cursor.execute(create_apartments_table)
connection.commit()

sql = """
INSERT INTO
  apartments (address, size, price)
VALUES(?,?,?)
"""

# find apartments on website
url = "https://ingatlan.com/lista/elado+budapest+lakas?page=1"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

count = 0
total = 0
entries = soup.find_all("div", class_="listing__card")
while entries:
	for entry in entries:
		if total%1000 == 0: print(count, total)
		total += 1
		try:
			if not entry.find("div", class_="listing__label label--newly-built"):
				address = entry.find("div", class_="listing__address").string.strip()
				address = address.replace(" kerület","")
				interior_size = entry.find("div", class_="listing__parameter listing__data--area-size").string
				interior_size = int(interior_size.replace("m² terület", ""))
				price = float(entry.find("div", class_="price").string.strip("M Ft"))
				#link = "ingatlan.com" + entry.find("a", class_="listing__link js-listing-active-area")["href"]
				count += 1
				data = (address, interior_size, price )
				new_apartment(connection, sql, data)
		except: print("Error on entry %s" % total)
			
	# load next page and repeat
	ind = url.find("=")+1
	next_page = int(url[ind:])+1
	url = url[:ind]+str(next_page)
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(req)
	html = page.read().decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")
	entries = soup.find_all("div", class_="listing__card")




