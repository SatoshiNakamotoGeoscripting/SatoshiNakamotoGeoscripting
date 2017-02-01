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
from os import system
sys.setdefaultencoding('utf8')

def getTweetsFromDB(dbname, username, password, tweet_table_name):
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, username, password))
    cursor = conn.cursor()
    
    # Retrieve data from database and extract coordinates
    cursor.execute("SELECT * FROM {}".format(tweet_table_name)) 
    records = cursor.fetchall()
    
    conn.close()
    cursor.close()
    return records

def importPolyJSON(dbname, username, password, geojson, output_table_name):
    """Import specified geojson file into postgresql spatial db"""
    # http://gis.stackexchange.com/questions/172092/import-geojson-into-postgis
    # http://morphocode.com/using-ogr2ogr-convert-data-formats-geojson-postgis-esri-geodatabase-shapefiles/
    bash = 'ogr2ogr -f "PostgreSQL" PG:"dbname={dbname} user={user}" "{geojson}" -nln {output_table_name}'.format(
            dbname = dbname,
            user = username,
            geojson = geojson,
            output_table_name = output_table_name)
    system(bash)

def getPointsPerPolygon(dbname, username, password, poly_table_name, tweet_table_name):
    """Perform spatial query to count statistics per table. Expects same SRS"""
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, username, password))
    cur = conn.cursor()
    
    # Geometry gets loaded at EWKB, which has to be decoded into geom format before PostGIS can use it.
    # The XY-coords derived from the tweets have to be referenced using ST_MakePoint
    sql ="""SELECT countrydata.name,
                   NULLIF(count({points}.id), 0)::int as NumOfTweets,
                   avg({points}.sentiment) as avgsentiment,
                   ST_X(ST_Centroid(ST_GeomFromEWKB({poly}.wkb_geometry))) as lon,
                   ST_Y(ST_Centroid(ST_GeomFromEWKB({poly}.wkb_geometry))) as lat,
                   countrydata.wkb_geometry
              FROM {poly}
              JOIN {points} ON ST_Intersects(ST_GeomFromEWKB({poly}.wkb_geometry), ST_SetSrid(ST_MakePoint({points}.loclong, {points}.loclat),4326))
              GROUP BY {poly}.name, countrydata.wkb_geometry
         """.format(poly = poly_table_name, points = tweet_table_name)  
    
    # Perform spatial query to count statistics per table
    cur.execute("DROP TABLE IF EXISTS temp; CREATE TABLE temp AS " + sql) # Deletes table if it exists, then recreates it
    conn.commit()
    
    cur.execute(sql)
    records = cur.fetchall()  
    
    # Retrieve table headers
    headers = [desc[0] for desc in cur.description]
    
    # Make pandas dataframe
    poly_df = pandas.DataFrame(records, columns = headers)    
    
    # Terminate connection calls
    conn.close()
    cur.close()
    
    return poly_df
    
def exportPostgresqltoGeojson(dbname, username, password, output_filename):
    # Export temporary table to GeoJSON
    bash = 'ogr2ogr -f "GeoJSON" {geojson}.geojson PG:"dbname={dbname} user={user} password={password}" "temp"'.format(
        dbname = dbname,
        user = username,
        password = password,
        geojson = output_filename)    
    system(bash)

def mapFromTweets(all_tweets, output_html_name = "tweet_map", polygon_geojson = False, polygon_data = False, zoom_start = 3, save = True, tiles = 'Stamen Terrain'):
    """From a list of tweets, derive the lat/lon and create a Folium map"""
    
    #TODO: implement sources
    #https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/
    #http://deparkes.co.uk/2016/06/24/folium-marker-clusters/

    # Select relevant data from all returned records for marker assignment
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
    
    # Get the center of the map by deriving the mean of all lats/longs
    mean_long = mean([tweet[-1][0] for tweet in list_of_tweets])
    mean_lat = mean([tweet[-1][1] for tweet in list_of_tweets])    
    
    world_geojson = r'countries.geo.json'
    tweet_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_start, tiles = tiles)
    
    # Make polygon layers with data
    if polygon_geojson != False and type(polygon_data) != bool:

        # Make an exponential colour ramp
        value_ramp = list(reversed([mean(polygon_data['numoftweets'])/i for i in range(1,6)]))
           
        tweet_map.choropleth(geo_path = polygon_geojson, data = polygon_data,
             columns=['name', 'numoftweets'],
             threshold_scale = value_ramp,
             key_on='feature.properties.name',
             fill_color='BuPu', fill_opacity=0.7, line_opacity=0.5,
             legend_name = 'number of tweets',
             reset=True)
            
        tweet_map.choropleth(geo_path = polygon_geojson, data = polygon_data,
             columns=['name', 'avgsentiment'],
             threshold_scale = [-0.25, -0.125, 0, 0.125, 0.25],
             key_on = 'feature.properties.name',
             fill_color = 'RdYlGn', fill_opacity = 0.7, line_opacity = 0.5, # Supported palettes: https://github.com/python-visualization/folium/pull/28/files
             legend_name = 'average sentiment',
             reset=True)
        
        # How do people come up with this stuff!??
        # https://github.com/python-visualization/folium/issues/458
        countries = folium.FeatureGroup(name="Countries")
        
        for lat, lon, name, avgsentiment in zip(polygon_data['lat'], polygon_data['lon'], polygon_data['name'], polygon_data['avgsentiment']):
            countries.add_child(folium.RegularPolygonMarker(
                location=[lat,lon],
                fill_color='#fffff',
                number_of_sides=4,
                radius=12,
                fill_opacity = 0.6,
                popup = folium.Popup(folium.element.IFrame(
                    html="<b>Country:</b> {} <br> <b>sentiment:</b> {:1.6s}".format(name, str(avgsentiment)),
                    width=200, height=100),
                    max_width=200)))
        
        tweet_map.add_child(countries)
    elif type(polygon_data) != bool:
        tweet_map.geo_json(geo_path = polygon_geojson, fill_color='#132b5e')
        
    
    # Create points to plot onto the map    
    tweet_cluster = folium.MarkerCluster("Tweets").add_to(tweet_map)
    
    for tweet in list_of_tweets:
        tweet_text = tweet[0]
        sentiment = tweet[1]        
        coords = tweet[-1]
        # html rendering source: http://stackoverflow.com/questions/29535715/python-with-folium-how-can-i-embed-a-webpage-in-the-popup
        html =  r"""{text} <br>
                <b> sentiment: </b>{sentiment}, {power} <br>
                <b> accurate location? </b> {accuracy} 
                """.format(text = tweet_text, accuracy = coords[2], sentiment = sentiment[0], power = sentiment[1])
        folium.Marker([coords[0], coords[1]],
        popup = folium.Popup(folium.element.IFrame(
            html=html,
            width=250, height=250),
            max_width=250)).add_to(tweet_cluster)
     
    folium.LayerControl().add_to(tweet_map)

    if save == True:
        tweet_map.save("{}.html".format(output_html_name))
    return tweet_map
    
tweets = getTweetsFromDB(dbname = "tweets",
                         username = "user",
                         password = "user",
                         tweet_table_name = "trumptweets2")[:10]
                         
importPolyJSON(dbname = "tweets",
               username = "user",
               password = "user",
               geojson = "world.geo.json",
               output_table_name = "countrydata")

records = getPointsPerPolygon(dbname = "tweets",
                              username = "user",
                              password = "user",
                              poly_table_name = "countrydata",
                              tweet_table_name = "trumptweets2")
                              
exportPostgresqltoGeojson(dbname = "tweets",
                          username = "user",
                          password = "user",
                          output_filename = "tweetspercountry")                              
                              
mapFromTweets(all_tweets = tweets,
              output_html_name = "trumptweets2",
              polygon_geojson = "tweetspercountry.geojson",
              polygon_data = records,
              save = True,
              tiles = "Stamen Terrain")
