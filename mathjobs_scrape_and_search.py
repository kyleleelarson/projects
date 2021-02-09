# scrape job postings from mathjobs.org
# and implement search feature

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

class job_listing:
	def __init__(self, title = "", type = "", location = "", area = "", description = ""):
		self.title = title
		self.type = type
		self.location = location
		self.area = area
		self.description = description
		
# load page with list of postings
url = "https://www.mathjobs.org/jobs?joblist-0-0------"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
postings = soup.find_all("li", class_=None)
print("Found {} postings. Loading now...".format(len(postings)))

# visit each posting and extract relevant data
# create list of job_listing objects
listings = []
for i, posting in enumerate(postings):
	if i % 25 == 0: print(i, end=' ', flush=True)
	if postings[i].find("a"):
		address = "https://www.mathjobs.org/" + postings[i].find("a")["href"]
		listing_page = urlopen(address)
		listing_html = listing_page.read().decode("utf-8")
		listing_soup = BeautifulSoup(listing_html, "html.parser")
		attr = []
		# handle position title separately
		attr.append(listing_soup.find("h2").get_text())
		for string in ["Type:", "Location:", "Area"]:
			text = ""
			string_start_idx = listing_html.find(string)
			# if posting contains item
			if string_start_idx != -1: 
				text_start_idx = string_start_idx + len(string) + 5
				offset = listing_html[text_start_idx:].find("<br>")
				text_end_idx = text_start_idx + offset
				text += listing_html[text_start_idx : text_end_idx]
				text = re.sub("\[.*?\]", "", text)
			attr.append(text)
		# now handle position description separately
		attr.append(listing_soup.find("tr").get_text())
		# initialize job_listing object
		listings.append(job_listing(attr[0],attr[1],attr[2],attr[3],attr[4]))

		
# allow user to search job postings
print("\nLoading complete.")
while True:
	answer = input("Would you like to search results? (Enter 'y' or 'n'. 'n' exits program.): ")
	if answer == "n": exit()
	matched = []
	
	# specify type
	type = input("""Select type. Enter 'a' for all, 'nt' for Non tenure-track faculty,
'p' for Postdoctoral, 't' for Tenured/Tenure-track faculty, or 'o' for all others: """)
	if type == "a": matched = listings
	else:
		type_dict = {'nt' : 'Non tenure-track faculty', 'p' : 'Postdoctoral',
			't' : 'Tenured/Tenure-track faculty'}
		if type in type_dict:
			for listing in listings:
				if listing.type == type_dict[type]:
					matched.append(listing)
		else: # 'o' for all others
			for listing in listings:
				if (listing.type != 'Non tenure-track faculty' and listing.type != 'Postdoctoral' 
					and listing.type != 'Tenured/Tenure-track faculty'):
					matched.append(listing)
	print("For the following fields, the entire (case-insentive) string will be matched. They may be left blank.")
	# search location
	location = input("Enter a term to search for in location: ")
	keep1 = []
	for listing in matched:
		if location.lower() in listing.location.lower():
			keep1.append(listing)
	matched = keep1
	
	# search description
	description = input("Enter a term to search for in description: ")
	keep2 = []
	for listing in matched:
		if description.lower() in listing.description.lower():
			keep2.append(listing)
	matched = keep2
	
	# search area
	area = input("Enter a term to search for in subject area: ")
	keep3 = []
	for listing in matched:
		if area.lower() in listing.area.lower():
			keep3.append(listing)
	matched = keep3
	
	print("******************************** search results ********************************")
	print("Total found: {}".format(len(matched)))
	answer = input("Would you like view the results? (Enter 'y' or 'n'.): ")
	if answer == "y":
		print("")
		for match in matched:
			print(match.title)
			print(match.type)
			print(match.area)
			print(match.location+'\n')

