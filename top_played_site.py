import os
import sys
import spotipy
import webbrowser
import spotipy.util as util
from flask import Flask, request
import psycopg2
from spotipy import oauth2

client_id = '980378f790cb40f595ecebedd58691f8'
client_secret = '365553ea22a64893b758fa2d2f8a79f0'
redirect_uri = 'http://10.0.0.251:5000/'
scope = 'user-read-birthdate, user-read-email, user-top-read'
cache = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope,cache_path=cache)

con = psycopg2.connect(
        host = "127.0.0.1",
        database = 'spotify_top',
        user = 'postgres',
        password = 'LoLpwnt11!')

cur = con.cursor()

app = Flask(__name__)

@app.route('/')
def index():

    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print('Access token available! Trying to get user information...')
        global sp
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return mid()
    else:
        return htmlforloginbutton()

def htmlforloginbutton():
    auth_url = getspoauthuri()
    htmlloginbutton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlloginbutton

def getspoauthuri():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

def mid(sp):

    user = sp.current_user()
    first_name, last_name = user['display_name'].split(' ', 1)
    email = user['email']
    birthdate = user['birthdate']
    follwers = user['followers']['total']
    userid = user['id']
    try:
        insert_var =  'INSERT INTO users (userid, first_name, last_name, email, birthdate, followers) VALUES (%s,%s,%s,%s,%s,%s)'
        insert_values = (userid, first_name, last_name, email, birthdate, followers)
        cur.execute(insert_var, insert_values)
        con.commit()

    except:
        update_var = 'UPDATE'
    short_term = sp.current_user_top_artists(limit=50, offset=0, time_range='short_term')
    short_term_results = short_term['items']

    short_html = ''

    b = 0
    for name in short_term_results:
        short_html += '<h4>' + str(b + 1) + ". " + short_term_results[b]['name']
        b = b+1

    medium_term = sp.current_user_top_artists(limit=50, offset=0, time_range='medium_term')
    medium_term_results = medium_term['items']

    medium_html = ''

    a = 0
    for name in medium_term_results:
        medium_html += '<h4>' + str(a + 1) + ". " + medium_term_results[a]['name']
        a = a+1


    long_term = sp.current_user_top_artists(limit=50, offset=0, time_range='long_term')
    long_term_results = long_term['items']

    long_html = ''

    c = 0
    for name in long_term_results:
        long_html += '<h4>' + str(c + 1) + '. ' + long_term_results[c]['name']
        c = c+1

    site = '<h1>Last 1 week:</br>' + short_html + '<h1>Last 6 months:</br>' + medium_html + '<h1>Last 5 Years:</br>' + long_html
    print(user)
    print(user['display_name'] + " - " + user['email'] + " - " +user['birthdate'])
    return site
    con.close()

app.route('/saving')
def mid():

    user = sp.current_user()
    first_name, last_name = user['display_name'].split(' ', 1)
    email = user['email']
    birthdate = user['birthdate']
    follwers = user['followers']['total']
    userid = user['id']
    try:
        insert_var =  'INSERT INTO users (userid, first_name, last_name, email, birthdate, followers) VALUES (%s,%s,%s,%s,%s,%s)'
        insert_values = (userid, first_name, last_name, email, birthdate, followers)
        cur.execute(insert_var, insert_values)
        con.commit()

    except:
        update_var = 'UPDATE'
    short_term = sp.current_user_top_artists(limit=50, offset=0, time_range='short_term')
    short_term_results = short_term['items']

    short_html = ''

    b = 0
    for name in short_term_results:
        short_html += '<h4>' + str(b + 1) + ". " + short_term_results[b]['name']
        b = b+1

    medium_term = sp.current_user_top_artists(limit=50, offset=0, time_range='medium_term')
    medium_term_results = medium_term['items']

    medium_html = ''

    a = 0
    for name in medium_term_results:
        medium_html += '<h4>' + str(a + 1) + ". " + medium_term_results[a]['name']
        a = a+1


    long_term = sp.current_user_top_artists(limit=50, offset=0, time_range='long_term')
    long_term_results = long_term['items']

    long_html = ''

    c = 0
    for name in long_term_results:
        long_html += '<h4>' + str(c + 1) + '. ' + long_term_results[c]['name']
        c = c+1

    site = '<h1>Last 1 week:</br>' + short_html + '<h1>Last 6 months:</br>' + medium_html + '<h1>Last 5 Years:</br>' + long_html
    print(user)
    print(user['display_name'] + " - " + user['email'] + " - " +user['birthdate'])
    return site
    con.close()
