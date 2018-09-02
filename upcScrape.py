import requests
import mysql.connector
from bs4 import BeautifulSoup
import urllib.request

#The UPC will be injected in the URL to lookup information about the product
upc = input("UPC of the game/system: ")

url = ("https://www.pricecharting.com/search-products?type=videogames&q=" + upc + "&go=Go")

response = requests.get(url)

html = response.text
soup = BeautifulSoup(html, "html.parser")
used_price = soup.find("span", {"class": "price js-price"})

#Strips any unwanted information from the string
used_price = used_price.text
used_price = used_price.replace(" ", "")
used_price = used_price.replace("$","")
used_price = float(used_price)

print (used_price)


cover = BeautifulSoup(html, "lxml")
game_cover = cover.find("div", {"id": "product_details"})
box_art = game_cover.findAll('img')

for image in box_art:
	pass

box_art_url = image.get("src")
box_art_url = ("https://www.pricecharting.com" + box_art_url)
print(box_art_url)