#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:02:08 2017

@author: user
"""

import psycopg2
from numpy import mean
import folium
import pandas
import sys  
reload(sys) #Prevents errors with utf-8 encoding not working properly
sys.setdefaultencoding('utf8')
from os import system

def getPointsPerPolygon(dbname, username, password, poly_table_name, tweet_table_name):
    """Perform spatial query to count statistics per table. Expects same SRS"""
    con = psycopg2.connect("dbname={} user={} password={}".format(dbname, username, password))
    cur = con.cursor()
    
    # Geometry gets loaded at EWKB, which has to be decoded into geom format before PostGIS can use it.
    # The XY-coords derived from the tweets have to be referenced using ST_MakePoint
    sql ="""SELECT countrydata.name,
                   NULLIF(count({points}.id), 0)::int as NumOfTweets,
                   avg({points}.sentiment) as avgsentiment,
                   ST_X(ST_Centroid(ST_GeomFromEWKB({poly}.wkb_geometry))) as lon,
                   ST_Y(ST_Centroid(ST_GeomFromEWKB({poly}.wkb_geometry))) as lat,
                   countrydata.wkb_geometry
              FROM {poly}
              JOIN {points} ON ST_Intersects(ST_GeomFromEWKB({poly}.wkb_geometry),
                               ST_SetSrid(ST_MakePoint({points}.loclong, {points}.loclat),4326))
              GROUP BY {poly}.name, countrydata.wkb_geometry
         """.format(poly = poly_table_name, points = tweet_table_name)  
    
    # Perform spatial query to count statistics per table
    cur.execute("DROP TABLE IF EXISTS polygonStatistics; CREATE TABLE polygonStatistics AS " + sql) # Deletes table if it exists, then recreates it
    con.commit()
    
    cur.execute(sql)
    records = cur.fetchall()  
    con.commit()
    
    # Retrieve table headers
    headers = [desc[0] for desc in cur.description]
    
    # Make pandas dataframe
    poly_df = pandas.DataFrame(records, columns = headers)    
    
    # Terminate connection calls
    con.close()
    cur.close()
    return poly_df
    
def filterTweetsToData(all_tweets):
    """Select relevant data from all returned records for marker assignment"""
    # TODO: Use pandas Dataframe as data sharing mechanism for direct column name assignment
    list_of_tweets = []
    for i, record in enumerate(all_tweets):
        tweet_text = record[11].encode('utf-8')
        tweet_sentiment_overall = record[14]
        tweet_label = record[15]
        
        
        # If it can use accurate coordinates, add these coordinates and True, else the estimated coords with False
        if record[2] != 9999:
            tweet_coords = (float(record[2]),float(record[3]), True)
        else:
            tweet_coords = (float(record[12]),float(record[13]), False)
        
        list_of_tweets.append([tweet_text, (tweet_sentiment_overall, tweet_label), tweet_coords])
    return list_of_tweets

class tweetMap:
    def __init__(self, list_of_tweets, zoom_start, tiles):
        self.list_of_tweets = list_of_tweets
        self.mean_long = mean([tweet[-1][0] for tweet in list_of_tweets])
        self.mean_lat = mean([tweet[-1][1] for tweet in list_of_tweets])   
        # Map tiles reference: http://www.digital-geography.com/python-and-webmaps-folium/#.WJHFHmelt75
        self.map = folium.Map(location=[self.mean_long, self.mean_lat], zoom_start = zoom_start, tiles = tiles)

    def addPolygonCentroids(self, polygon_geojson, polygon_data):
        # How do people come up with this stuff!??
        # https://github.com/python-visualization/folium/issues/458
        countries = folium.FeatureGroup(name="Countries")
        for lat, lon, name, avgsentiment in zip(polygon_data['lat'], polygon_data['lon'], polygon_data['name'], polygon_data['avgsentiment']):
            countries.add_child(folium.RegularPolygonMarker(
                location=[lat,lon],
                fill_color='#00c5ff',
                number_of_sides=4,
                radius=6,
                fill_opacity = 0.4,
                popup = folium.Popup(folium.element.IFrame(
                    html="<b>Country:</b> {} <br> <b>sentiment:</b> {:1.6s}".format(name, str(avgsentiment)),
                    width=200, height=100),
                    max_width=200)))
        self.map.add_child(countries)

    def addChoropleths(self, polygon_geojson, polygon_data):
        """Adds choropleth layers to the map"""
        if polygon_geojson != False and type(polygon_data) != bool:
    
            # Make an exponential colour ramp
            self.map.choropleth(geo_path = polygon_geojson, data = polygon_data,
                 columns=['name', 'avgsentiment'],
                 threshold_scale = [-0.25, -0.125, 0, 0.125, 0.25],
                 key_on = 'feature.properties.name',
                 fill_color = 'RdYlGn', fill_opacity = 0.5, line_opacity = 0.5, # Supported palettes: https://github.com/python-visualization/folium/pull/28/files
                 legend_name = 'average sentiment',
                 reset=True)    
    
            # Create a value ramp by dividing with the mean, then make the numbers integers and ensure that there is a ramp-up
            value_ramp = list(reversed([mean(polygon_data['numoftweets'])/i for i in range(1,6)]))
            value_ramp = [int(i)+1 for i in value_ramp]
               
            self.map.choropleth(geo_path = polygon_geojson, data = polygon_data,
                 columns=['name', 'numoftweets'],
                 threshold_scale = value_ramp,
                 key_on='feature.properties.name',
                 fill_color='BuPu', fill_opacity=0.5, line_opacity=0.5,
                 legend_name = 'number of tweets',
                 reset=True)
                 
        elif type(polygon_data) != bool:
            self.map.geo_json(geo_path = polygon_geojson, fill_color='#132b5e')
    
    def addTweets(self):
        # Create points to plot onto the map    
        tweet_cluster = folium.MarkerCluster("Tweets").add_to(self.map)
        
        # Selects a colour based on the value found. Only 5 classes are present due to limited 
        colors_list = [[1,"blue"],[0.25,"purple"],[0,"green"],[-0.25,"orange"],[-1,"red"]]        
        color = "black"
        icon_color = "white"
        
        for tweet in self.list_of_tweets:
            tweet_text = tweet[0]
            sentiment = tweet[1]        
            coords = tweet[-1]  
            for i in range(len(colors_list)):
                if sentiment[1] != None:
                    if str(sentiment[1]) != '0.0':
                        if colors_list[i][0] >= sentiment[1] >= colors_list[i+1][0]:
                            color = colors_list[i+1][1]
                            icon_color = "white"
                    else:
                        color = "white"
                        icon_color = "black"
                else:
                    color = "black"
                    icon_color = "white"
                    
            # html rendering source: http://stackoverflow.com/questions/29535715/python-with-folium-how-can-i-embed-a-webpage-in-the-popup
            html =  r"""{text} <br>
                    <b> sentiment: </b>{sentiment}, {power} <br>
                    <b> accurate location? </b> {accuracy} 
                    """.format(text = tweet_text, accuracy = coords[2], sentiment = sentiment[0], power = sentiment[1])
            folium.Marker([coords[0], coords[1]],
                    icon = folium.Icon(color=color, icon_color=icon_color),
                    popup = folium.Popup(folium.element.IFrame(
                        html=html,
                        width=250, height=250),
                        max_width=250)).add_to(tweet_cluster)
                
    def addLayerControl(self):
        folium.LayerControl().add_to(self.map)    
    
    def saveMap(self, output_html_name):
        self.map.save("{}.html".format(output_html_name))

