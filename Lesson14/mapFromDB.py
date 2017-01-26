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

def getTweets(dbname, user, password, table_name):
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, user, password))
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    # execute our Query
    cursor.execute("SELECT * FROM {}".format(table_name)) 
    # retrieve the records from the database
    records = cursor.fetchall()
    values=[]
    for i in range(len(records)):
        tweet_text = records[i][11].encode('utf-8')
        # Get lat/lon
        values.append((float(records[i][12]),float(records[i][13]), tweet_text))
    return values

def mapFromDB(tweets, outname, zoom_level, save = True, tiles = 'Stamen Terrain'):
    #Get the center of the map by deriving the mean of all lats/longs
    mean_long = mean([pt[0] for pt in tweets])
    mean_lat = mean([pt[1] for pt in tweets])
    point_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_level, tiles = tiles)
    for pt in tweets:
        folium.Marker([pt[0], pt[1]],\
        popup = folium.Popup(folium.element.IFrame(
        html='''
                <b>Tweet:</b>  {tweet}<br>
             '''.format(tweet = pt[2]),\
        width=250, height=150),\
        max_width=250)).add_to(point_map)
    if save == True:
        point_map.save("{}.html".format(outname))
    return point_map
tweets = getTweets("tweets","user","user","drugtable")
mapFromDB(tweets, 'drugTweets', 3, save = True, tiles = 'Stamen Terrain')