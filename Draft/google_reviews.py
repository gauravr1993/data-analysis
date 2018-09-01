import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

url = 'https://play.google.com/store/apps/collection/promotion_30017ea_starterkit_games'
resp = requests.get(url)
html = resp.text

domain = "https://play.google.com"
review_url = '&showAllReviews=true'

soup = BeautifulSoup(html,'lxml')

app_name = [app['title'] for app in soup.select('a.title')]
studio_name = [studio['title'] for studio in soup.select('a.subtitle')]
game_desc = [desc.contents[0] for desc in soup.select('div.description')]
rating_text = [text['aria-label'] for text in soup.select('div.tiny-star')]
rating = []
rating = [el.split()[1] for el in rating_text]
app_link = [desc['href'] for desc in soup.select('a.title')]
req_url = domain + app_link[0] + review_url

print app_name

review_resp = requests.get(req_url)
print req_url
reviews_text = review_resp.text

soup2 = BeautifulSoup(reviews_text,'lxml')

#print soup2
reviews = [el.text for el in soup2.find('span')]
print reviews
