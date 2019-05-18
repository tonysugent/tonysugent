#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as BS
import os
import smtplib
import pandas as pd
import re
from email.mime.text import MIMEText
url = 'https://annarbor.craigslist.org/'
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X)'}
response = requests.get(url, headers=headers)

search = url + 'search/sss'

def find_cars(max_price, make):
    search_params = {'sort': 'rel',
                     'min_price': '50',
                     'max_price': max_price,
                     'query': make,
                     'auto_transmission': '1',
                     'srchType': 'T'}


    r = requests.get(search, params=search_params, headers=headers)
    s = BS(r.content, 'html.parser')
    c = s.prettify
    price_list = []
    title_list = []
    link_list = []
    for i,a in enumerate(s.find_all('p', {'class': 'result-info'})):
        price = a.find('span', {'class': 'result-price'}).text
        title = a.find('a', {'class': 'result-title'}).text
        link = a.find('a', attrs={'href': re.compile("^https://")})

        if i < 20:
            price_list.append(price)
            title_list.append(title)
            link_list.append(link.get('href'))
    z = 0
    pd.set_option('display.max_colwidth', -1)
    cars = pd.DataFrame({'Car':title_list, 'Price': price_list, 'Link': link_list})

    return(cars.to_html())

def email(message):
    gmail_user = 'tony.sugent@gmail.com'
    gmail_password = 'xxxxxxxxxxxxxxx'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:
        print('Whoops....')

    server.sendmail('tony.sugent@gmail.com','tony.sugent@gmail.com', msg=message)

msg = find_cars('20000','Volkswagen')
msg = MIMEText(msg, 'html')

email(msg.as_string())
