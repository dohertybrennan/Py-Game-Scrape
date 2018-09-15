#!/usr/bin/python3
import sys
import requests
import mysql.connector as mycon
from bs4 import BeautifulSoup
import urllib.request
import os.path
from urllib.request import urlopen as uReq

#Connection to database
mydb = mycon.connect(
	host="localhost",
	user="wpuser",
	passwd="supersecretpassword",
	database="vgdb"
)


def gameInfo(x):

	#Checks to see if gameinfo already exists in database
	cursor = mydb.cursor()
	cursor.execute("select exists (select * from vgdb where upc = '" + x + "');")
	result = cursor.fetchone()

	if result[0] == 0:
		print("Game not in Database. Retrieving info online...\n")
		#This game is not in the database and info will now be retrieved
		url = ("https://www.pricecharting.com/search-products?type=videogames&q=" + x + "&go=Go")
		response = uReq(url)
		html = response.read()
		response.close()
		soup = BeautifulSoup(html, "html.parser")

		#Defines where to look for the information on the webpage
		full_details = soup.find("div", {"id": "full_details"})
		title = soup.find("div", {"class": "recommendations horizontal js-recommendations"})
		console_raw = soup.find("h1", {"class": "chart_title"})

		#Tries to catch an error with loading the webpage
		if title is not None:
			title = title.text
			title = title.replace("Buy ", "")
			title = title.strip()
		else:
			print("An error has occurred")
			exit()

		#Pulls all fo the details about the game at the bottom of the page into an array
		details = full_details.findAll('span')
		detail_list = []
		for detail in details:
			detail_list.append(detail.text)

		genre = detail_list[1].strip()
		release_date = detail_list[3].strip()
		esrb = detail_list[5].strip()

		cursor.execute('insert into vg_test values ("' + x + '", "' + title + '", "' + genre + '", "' + release_date + '");')
		mydb.commit()

		cursor.execute('select * from vg_test where upc =' + x + ';')
		result = cursor.fetchone()

		title = result[1]
		genre = result[2]
		release_date = result[3]

		console = console_raw.find("a")
		console = console.text

		full_details = "UPC: " + x + "\nTitle: " + title +"\nGenre: " + genre +"\nRelease Date: " + release_date + "\nConsole: " + console
		print(full_details)

		cover = BeautifulSoup(html, "lxml")
		game_cover = cover.find("div", {"id": "product_details"})
		box_art = game_cover.findAll('img')

		for image in box_art:
			pass

		box_art_url = image.get("src")
		box_art_url = ("https://www.pricecharting.com" + box_art_url)
		local_image_name = ("images/" + title + " " + console + ".jpg").replace(" ", "-").lower()

		urllib.request.urlretrieve(box_art_url, local_image_name)
		print("Saving box art as " + local_image_name)

	elif result[0] == 1:
		print("Retrieving Game Info from the Database...\n")
		cursor.execute('select * from vg_test where upc =' + x + ';')
		result = cursor.fetchone()

		title = result[1]
		genre = result[2]
		release_date = result[3]

		full_details = "UPC: " + x + "\nTitle: " + title +"\nGenre: " + genre +"\nRelease Date: " + release_date
		print(full_details)

	else:
		print("There has been an error. Please contact your administrator")


def upcLookup(x):

	web_search = ("https://www.pricecharting.com/search-products?q=" + x + "&type=videogames")
	response = requests.get(web_search)
	html = response.text
	soup = BeautifulSoup(html, "lxml")

	page_test = soup.find("h1")
	game_title = soup.find("td", {"class": "title"})
	game_link = game_title.find('a')

	if page_test.text == x.replace("+", " ") + " Prices":
		for x in game_link:
			pass
		next_page = game_link.get("href")

		response = requests.get(next_page)
		html = response.text


	soup = BeautifulSoup(html, "html.parser")
	full_details = soup.find("div", {"id": "full_details"})
	details = full_details.findAll('span')
	detail_list = []
	for detail in details:
		detail_list.append(detail.text)

	upc = detail_list[7].strip()
	return upc



#The UPC will be injected in the URL to lookup information about the product
upc = sys.argv[1]

if upc == "0":
	title = sys.argv[2]
	console = sys.argv[3]
	web_query = title.replace("-", "+") + "+" + console.replace("-", "+")
	upc = upcLookup(web_query)
	print(len(upc))
	if len(upc) > 12:
		upc = upc.split(",")
		print(upc[0])
		print(int(upc[1]))

		for x in upc:
			gameInfo(x)

	else:
		gameInfo(upc)
else:
	gameInfo(upc)
