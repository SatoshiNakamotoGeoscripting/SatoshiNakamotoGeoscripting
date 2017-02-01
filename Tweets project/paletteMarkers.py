#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 09:42:58 2017

@author: user
"""
import folium
import psycopg2
import sys
reload(sys) #Prevents errors with utf-8 encoding not working properly
sys.setdefaultencoding('utf8')
from numpy import mean

def getTweetsFromDB(dbname, username, password, table_name):
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, username, password))
    cursor = conn.cursor()
    
    # Retrieve data from database and extract coordinates
    cursor.execute("SELECT * FROM {} WHERE lang = 'en'".format(table_name)) 
    records = cursor.fetchall()
    
    list_of_tweets = []
    for i, record in enumerate(records):
        tweet_text = record[11].encode('utf-8')
        tweet_label = record[14]
        tweet_sentiment = float(record[15])

        # If it can use accurate coordinates, add these coordinates and True, else the estimated coords with False
        if record[2] != 9999:
            tweet_coords = (float(record[2]),float(record[3]), True)
        else:
            tweet_coords = (float(record[12]),float(record[13]), False)
        
        list_of_tweets.append([tweet_text, tweet_coords, tweet_label, tweet_sentiment])
    conn.close()
    cursor.close()
    return list_of_tweets

tweets = getTweetsFromDB("tweets","user","user","trumptweets2")



def mapFromTweets(list_of_tweets, output_file_name, zoom_start = 3, save = True, tiles = 'Stamen Terrain'):
    """From a list of tweets, derive the lat/lon and create a Folium map"""
    
    #TODO: implement sources
    #https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/
    #http://deparkes.co.uk/2016/06/24/folium-marker-clusters/
    
    # Get the center of the map by deriving the mean of all lats/longs
    # NOTE: "fit_bounds() builtin not working, so defaulted to using mean lat/long
    mean_long = mean([tweet[1][0] for tweet in list_of_tweets])
    mean_lat = mean([tweet[1][1] for tweet in list_of_tweets])
    
    world_geojson = r'countries.geo.json'
    tweet_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_start, tiles = tiles)
    tweet_map.geo_json(geo_path = world_geojson, fill_color='#132b5e')
    tweet_cluster = folium.MarkerCluster("tweets").add_to(tweet_map)
    
    colors_list = [[1,"blue"],[0.5,"purple"],[0.0,"black"],[-0.5,"orange"],[-1,"red"]]
    
    for tweet in tweets:        
        tweet_text = tweet[0]
        coords = tweet[1]
        # html rendering source: http://stackoverflow.com/questions/29535715/python-with-folium-how-can-i-embed-a-webpage-in-the-popup
        color = 'green'
        for i in range(len(colors_list)):
            if colors_list[i][0] >= tweet[3] >= colors_list[i+1][0]:
                color = colors_list[i+1][1]
        #print tweet[3],color
                
        html =  r"""{text} <br>""".format(text = tweet_text)
        folium.Marker([coords[0], coords[1]],
            icon = folium.Icon(color=color),
            popup = folium.Popup(folium.element.IFrame(
                                html=html,
                                width=250, height=250),
                                max_width=250)).add_to(tweet_cluster)
    if save == True:
        tweet_map.save("{}.html".format(output_file_name))
    return tweet_map

mapFromTweets(tweets,"trumptweets", save = True, tiles = "Stamen Terrain")
