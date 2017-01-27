#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:02:08 2017

@author: user
"""

import psycopg2
from numpy import mean
import folium
import sys  
reload(sys) #Prevents errors with utf-8 encoding not working properly
sys.setdefaultencoding('utf8')

def getTweetsFromDB(dbname, user, password, table_name):
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, user, password))
    cursor = conn.cursor()
    
    # Retrieve data from database and extract coordinates
    cursor.execute("SELECT * FROM {}".format(table_name)) 
    records = cursor.fetchall()
    
    list_of_tweets = []
    for i, record in enumerate(records):
        tweet_text = record[11].encode('utf-8')
        tweet_url = record[10].encode('utf-8')

        # If it can use accurate coordinates, add these coordinates and True, else the estimated coords with False
        if record[2] != 9999:
            tweet_coords = (float(record[2]),float(record[3]), "Yes")
        else:
            tweet_coords = (float(record[12]),float(record[13]), "No")
        
        list_of_tweets.append([tweet_text, tweet_url, tweet_coords])
    return list_of_tweets

def mapFromTweets(list_of_tweets, output_file_name, zoom_level, save = True, tiles = 'Stamen Terrain'):
    """From a list of tweets, derive the lat/lon and create a Folium map"""
    
    #TODO: implement sources
    #https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/
    #http://deparkes.co.uk/2016/06/24/folium-marker-clusters/
    #https://github.com/python-visualization/folium    
    """Fit bounds"""
    
    # Get the center of the map by deriving the mean of all lats/longs
    mean_long = mean([tweet[2][0] for tweet in list_of_tweets])
    mean_lat = mean([tweet[2][1] for tweet in list_of_tweets])
    
    # TODO: Get top-right & bot-left, then create three classes for zoom level
    world_geojson = r'countries.geo.json'
    tweet_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_level, tiles = tiles)
    tweet_map.geo_json(geo_path = world_geojson, fill_color='#132b5e')
    tweet_cluster = folium.MarkerCluster("tweets").add_to(tweet_map)
    
    for tweet in tweets:
        tweet_text = tweet[0]
        url = tweet[1]
        coords = tweet[2]
        # html rendering source: http://stackoverflow.com/questions/29535715/python-with-folium-how-can-i-embed-a-webpage-in-the-popup
        html =  r"""<b>Tweet:</b> {text}<br><br>
                    <b>Accurate location?</b> {accuracy}""".format(text = tweet_text, accuracy = coords[2])
        folium.Marker([coords[0], coords[1]],
        popup = folium.Popup(folium.element.IFrame(
            html=html,
            width=250, height=250),
            max_width=250)).add_to(tweet_cluster)
    if save == True:
        tweet_map.save("{}.html".format(output_file_name))
    return tweet_map
tweets = getTweetsFromDB("tweets","user","user","trumptweets")
mapFromTweets(tweets, 'trumptweets', 3, save = True, tiles = 'Stamen Terrain')