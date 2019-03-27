#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as BS

url = 'https://annarbor.craigslist.org/'
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X)'}
response = requests.get(url, headers=headers)

search = url + 'search/sss'

search_params = {'sort': 'rel',
                 'min_price': '50',
                 'query': 'Subaru',
                 'auto_transmission': '1',
                 'srchType': 'T'}


r = requests.get(search, params=search_params, headers=headers)
s = BS(r.content, 'html.parser')
c = s.prettify

price_list = []
title_list = []
loc_list = []
for i,a in enumerate(s.find_all('p', {'class': 'result-info'})):
    price = a.find('span', {'class': 'result-price'}).text
    title = a.find('a', {'class': 'result-title'}).text

    if i < 20:
        price_list.append(price)
        title_list.append(title)

z = 0

for i in title_list:
    print(title_list[z])
    print(price_list[z])
    print(loc_list[z])
    z= z+1
