import requests
import mysql.connector as mycon
from bs4 import BeautifulSoup
import urllib.request

website = input("Type the page in which to grab data from: ")
response = requests.get(website)
html = response.text
soup = BeautifulSoup(html, "lxml")

game_title = soup.find("td", {"class": "title"})
game_link = game_title.find('a')

for x in game_link:
	pass
next_page = game_link.get("href")
print(next_page)
