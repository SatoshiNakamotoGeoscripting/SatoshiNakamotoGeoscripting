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
reload(sys)  
sys.setdefaultencoding('utf8')
    

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect("host='localhost' dbname='lesson14' user='postgres' password='secret'")
# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
# execute our Query
cursor.execute("SELECT * FROM lesson14_barcelona") 
# retrieve the records from the database
records = cursor.fetchall() 
values=[]
for i in range(len(records)):
    tweet = records[i][5].encode('utf-8')
    values.append((float(records[i][3]),float(records[i][4]),tweet))
    

def mapFromDB(pts, outname, zoom_level, save = True, tiles = 'Stamen Terrain'):
    #Get the center of the map by deriving the mean of all lats/longs
    mean_long = mean([pt[0] for pt in pts])
    mean_lat = mean([pt[1] for pt in pts])
    point_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_level, tiles = tiles)
    for pt in pts:
        folium.Marker([pt[0], pt[1]],\
        popup = folium.Popup(folium.element.IFrame(
        html='''
                <b>Tweet:</b>  {tweet}<br>
             '''.format(tweet = pt[2]),\
        width=150, height=100),\
        max_width=150)).add_to(point_map)
    if save == True:
        point_map.save("{}.html".format(outname))
    return point_map

mapFromDB(values, 'BarcelonaTweets', 15, save = True, tiles = 'Stamen Terrain')


pts = values
mean_long = mean([pt[0] for pt in pts])
mean_lat = mean([pt[1] for pt in pts])
point_map = folium.Map(location=[mean_long, mean_lat], zoom_start = 10, tiles = 'Stamen Terrain')
for pt in pts:
    folium.Marker([pt[0], pt[1]],\
    popup = folium.Popup(folium.element.IFrame(
    html='''
            <b>Tweet:</b>  {tweet}<br>
         '''.format(tweet = pt[2]),\
    width=150, height=100),\
    max_width=150)).add_to(point_map)