#!/usr/bin/python3

import os
import sys
import json
import csv
import spotipy
import webbrowser
import spotipy.util as util
import matplotlib.pyplot as plt
import pandas as pd
import datetime

username=sys.argv[1]

try:
    token = util.prompt_for_user_token(username)

except:
    os.remove(".cache-username")
    token = util.prompt_for_user_token(username)

spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

displayname = user['display_name']
follower = user['followers']['total']
date = datetime.date.today()
date = date.strftime('%m.%d.%y')
similar = []
pop = []
followers = []

def graph():
    popularity = pd.read_csv('band_data.csv',index_col=False,encoding="utf-8-sig")

    popularity.pivot_table('Popularity','Date','Artists').plot(kind='line',marker='o')
    plt.xlabel('Popularity')
    plt.ylabel('Dates')
    plt.show()

def csvcreate():
    df = pd.DataFrame({'Artists':similar, 'Date':str(date), 'Popularity':pop})
    df.to_csv('band_data.csv',mode= 'a', index=False)
    graph()

def refresh():
    searchfor = "Drake"

    searchresults = spotifyObject.search(searchfor,1,0,"artist")
    artist = searchresults['artists']['items'][0]
    print(str(artist['followers']['total']) + " followers\n")
    print("Popularity: " + str(artist['popularity']))
    print()
    artistid = artist['id']
    related = spotifyObject.artist_related_artists(artistid)
    relatedartists = related['artists']
    z = 0

    for name in relatedartists:

        print("Name: " + related['artists'][z]['name'])
        print("Popularity: " + str(related['artists'][z]['popularity']))
        print("Followers: " + str(related['artists'][z]['followers']))
        print()
        similar.append(related['artists'][z]['name'])
        pop.append(int(related['artists'][z]['popularity']))
        followers.append(related['artists'][z]['followers'])
        z +=1

    print(similar)
    print(pop)
    csvcreate()

refresh()
