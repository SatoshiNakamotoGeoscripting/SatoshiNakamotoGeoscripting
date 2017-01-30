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
from os import system
sys.setdefaultencoding('utf8')

def getTweetsFromDB(dbname, username, password, source_table_name):
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
            tweet_coords = (float(record[2]),float(record[3]), True)
        else:
            tweet_coords = (float(record[12]),float(record[13]), False)
        
        list_of_tweets.append([tweet_text, tweet_url, tweet_coords])
    con.close()
    cursor.close()
    return list_of_tweets

def importPolyJSON(dbname, username, password, geojson, output_table_name):
    """Import specified geojson file into postgresql spatial db"""
    bash = 'ogr2ogr -f "PostgreSQL" PG:"dbname={dbname} user={user}" "{geojson}" -nln {output_table_name}'.format(
            dbname = dbname,
            user = username
            geojson = geojson
            output_table_name = output_table_name)
    system(bash)

def getPointsPerPolygon(dbname, username, password, poly_table_name, tweet_table_name):
    """Perform spatial query to count statistics per table. Expects same SRS"""
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, user, password))
    cursor = conn.cursor()
    
    # Perform spatial query to count statistics per table
    cursor.execute("""SELECT {poly}.name, avg({points}.sentiment), ST_WKT_from_geom({poly.geom})
                      FROM {poly}
                      JOIN {points} ON ST_Intersects({poly}.geom, {points}.geom)
                      GROUP BY {poly}.name
                   """.format(poly_table_name, tweet_table_name))
    records = cursor.fetchall()
    # TODO: Retrieve table and export to geojson
    
def mapFromTweets(list_of_tweets, output_file_name, zoom_start = 3, save = True, tiles = 'Stamen Terrain'):
    """From a list of tweets, derive the lat/lon and create a Folium map"""
    
    #TODO: implement sources
    #https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/
    #http://deparkes.co.uk/2016/06/24/folium-marker-clusters/
    
    # Get the center of the map by deriving the mean of all lats/longs
    # NOTE: "fit_bounds() builtin not working, so defaulted to using mean lat/long
    mean_long = mean([tweet[2][0] for tweet in list_of_tweets])
    mean_lat = mean([tweet[2][1] for tweet in list_of_tweets])
    
    world_geojson = r'countries.geo.json'
    tweet_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_start, tiles = tiles)
    tweet_map.geo_json(geo_path = world_geojson, fill_color='#132b5e')
    tweet_cluster = folium.MarkerCluster("tweets").add_to(tweet_map)
    
    for tweet in tweets:
        tweet_text = tweet[0]
        url = tweet[1]
        coords = tweet[2]
        # html rendering source: http://stackoverflow.com/questions/29535715/python-with-folium-how-can-i-embed-a-webpage-in-the-popup
        html =  r"""{text} <br>""".format(text = tweet_text)
        folium.Marker([coords[0], coords[1]],
        popup = folium.Popup(folium.element.IFrame(
            html=html,
            width=250, height=250),
            max_width=250)).add_to(tweet_cluster)
    if save == True:
        tweet_map.save("{}.html".format(output_file_name))
    return tweet_map
    
tweets = getTweetsFromDB("tweets","user","user","trumptweets")
importPolyJSON("tweets","user","user", "world.geo.json", "countrydata")
getPointsPerPolygon("tweets","user","user", "countrydata", "trumptweets")
mapFromTweets(tweets,"'trumptweets", save = True, tiles = "Stamen Terrain")