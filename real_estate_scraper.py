# web scraper for Hungarian real estate website ingatlan.com
# used to send daily alerts for new properties

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import date
import smtplib, ssl
import unidecode


# read old properties into string
f = open("gyula_houses.txt", "r")
previous_entries = f.read()
f.close()


# find new properties from website
url = "https://ingatlan.com/szukites/elado+haz+gyula?page=1"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
new_properties = ""
count = 0
total = 0
entries = soup.find_all("div", class_="listing__card")
while entries:
	for entry in entries:
		total += 1
		address = entry.find("div", class_="listing__address").string
		address = address.replace("Gyula, ", "").replace(", Gyula","").strip()
		output = address + (" "*(22-len(address)))
		interior_size = entry.find("div", class_="listing__parameter listing__data--area-size").string
		interior_size = interior_size.replace("m² terület", "sqm")
		output += (interior_size+(" "*(12-len(interior_size))))
		price = entry.find("div", class_="price").string.strip(" Ft")
		output += (price+(" "*(12-len(price))))
		link = "ingatlan.com" + entry.find("a", class_="listing__link js-listing-active-area")["href"]
		output += (link+"\n")
		if output not in previous_entries:
			new_properties += output
			count += 1
	# load next page and repeat		
	next_page = int(url[-1]) + 1
	url = url[:-1]+str(next_page)
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(req)
	html = page.read().decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")
	entries = soup.find_all("div", class_="listing__card")


# add new properties to file
today = date.today()
f = open("gyula_houses.txt", "a")
f.write("%s new properties of a total %s found on %s: \n" % (count,total,today))
f.write(new_properties+"\n")
f.close()


# send email with new properties
if count != 0:
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "*********@gmail.com"  
	recipients = ["*********@gmail.com", "*********@gmail.com"]
	password = "*********"
	subject= str(count)+" new Gyula properties for sale"
	text = unidecode.unidecode(new_properties)+"\n From: Ingatlan Robot \n"
	message = "Subject: {}\n\n{}".format(subject, text)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, recipients, message)