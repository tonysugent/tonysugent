from flask import Flask, g
import json
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from geopy.geocoders import Nominatim
import math

app = Flask(__name__)
app.run(host='0.0.0.0', port=80)

@app.route('/countries/')

def countries():
    url = 'https://en.wikipedia.org/wiki/Nuclear_power_by_country'
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    table = soup.find_all('table')
    df = pd.read_html(str(table), header=0)
    jsondata = json.loads(df[1].to_json(orient='records'))
    return(json.dumps(jsondata))

@app.route('/countries/current/<string:con>')

# Country Codes are = {Argentina: AR, Bangladesh: BD, Belarus: BY,
# Brazil: BR, China: CN, Finland: FL, }

def by_country(con):

    url = 'https://pris.iaea.org/PRIS/CountryStatistics/CountryDetails.aspx?current=' + con
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    table = soup.find_all('table')
    df = pd.read_html(str(table), header=0)
    jsondata = json.loads(df[3].to_json(orient='records'))

    return(json.dumps(jsondata))

@app.route('/closest/<string:address>')

def find_closest_reactor(address):

    geolocator = Nominatim(user_agent="api")
    add = geolocator.geocode(address)

    url = 'https://en.wikipedia.org/wiki/List_of_nuclear_power_stations'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find_all('table')
    df = pd.read_html(str(table), header=0, encoding='utf-8')

    drop_list = ['# units', 'Net capacity(MWe)', 'Country', 'Refs']

    lats_only = df[1].drop(drop_list, axis=1)
    lats_only['Location'] = lats_only['Location'].str.split("/", expand=False).str[1].str.replace('°', '')
    lats_only['Location'] = lats_only['Location'].str.split(" ", expand=False).str[1:]
    lats_only['Lat'] = lats_only['Location'].str[0]
    lats_only['Lon'] = lats_only['Location'].str[1]

    z = 0
    for i in lats_only['Lon']:
        if i.endswith('W'):
            i = i.replace('W', '')
            lats_only['Lon'][z] = -(float(i))
        else:
            i = i.replace('E', '')
            lats_only['Lon'][z] = float(i)
        z = z + 1

    g = 0
    for i in lats_only['Lat']:
        if i.endswith('S'):
            i = i.replace('S', '')
            lats_only['Lat'][g] = -(float(i.lstrip('\ufeff')))
        else:
            i = i.replace('N', '')
            lats_only['Lat'][g] = float(i.lstrip('\ufeff'))
        g = g + 1

    lats_only = lats_only.drop('Location', axis=1)

    user_location = (add.latitude, add.longitude)
    reactor_location = []
    h = 0
    for i in lats_only['Lat']:
        reactor_location.append(tuple((lats_only['Lat'][h], lats_only['Lon'][h])))
        h = h+1

    c = 0
    dist = []

    for i in reactor_location:
        dist.append(math.sqrt((user_location[0]-reactor_location[c][0])**2+(user_location[1]-reactor_location[c][1])**2))
        c = c+1

    lats_only['Dist'] = dist
    lats_only = lats_only.sort_values('Dist').reset_index()

    return(str(lats_only['Power station'][0]))

@app.errorhandler(404)
def page_not_found(error):
    return('Not Found'), 404
