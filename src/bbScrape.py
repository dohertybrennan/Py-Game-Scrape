#import requests
from urllib.request import urlopen as uReq
import mysql.connector
from bs4 import BeautifulSoup as soup

upc = input("UPC of the game/system: ")

url = ("https://www.bestbuy.com/site/searchpage.jsp?st=" + upc + "&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys")

response = uReq(url)
page_html = response.read()
response.close()

#print(page_html)

page_soup = soup(page_html, "html.parser")
price = page_soup.find("div", {"class": "priceView-hero-price priceView-purchase-price"})
price = price.text
price = price.replace("$", "")
price = float(price)

print(price)