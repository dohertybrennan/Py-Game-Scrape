#!/usr/bin/python3
import sys
import requests
import mysql.connector as mycon
from bs4 import BeautifulSoup
import urllib.request

#Connection to database
mydb = mycon.connect(
	host="localhost",
	user="brennan",
	passwd="admin",
	database="test"
)

def soldUsed(x):
	url = ("https://www.ebay.com/sch/i.html?_fsrp=1&_nkw=" + x + "&_sacat=0&_from=R40&LH_Complete=1&rt=nc&LH_Sold=1&LH_ItemCondition=4&_ipg=200")
	response = requests.get(url)
	html = response.text
	soup = BeautifulSoup(html, "html.parser")

	base_prices = soup.findAll("span", {"class": "POSITIVE"})
	shipping_costs = soup.findAll("span", {"class": "s-item__shipping s-item__logisticsCost"})

	base_price = []
	shipping_cost = []

	for y in base_prices:
		y = y.text
		y = y.replace(" to ", "0")
		y = y.replace("$", "")
		y = float(y)
		base_price.append(y)
		#print(y)

	for z in shipping_costs:
		if z.text == "Free Shipping":
			z = 0.00
			shipping_cost.append(z)
		else:
			z = z.text.replace("+$", "")
			z = z.replace(" shipping", "")
			z = float(z)
			shipping_cost.append(z)

	base_price.remove(max(base_price))
	avg_base_price = sum(base_price)/len(base_price)
	avg_base_price = round(avg_base_price,2)
	print(avg_base_price)

	avg_shipping_cost = sum(shipping_cost)/len(shipping_cost)
	avg_shipping_cost = round(avg_shipping_cost,2)
	print(avg_shipping_cost)

upc = sys.argv[1]

if upc == "0":
	title = sys.argv[2]
	console = sys.argv[3]
	web_query = title.replace("-", "+") + "+" + console.replace("-", "+")
	import vgScrape
	upc = vgScrape.upcLookup(web_query)
	soldUsed(upc)

else:
	soldUsed(upc)
