    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
import geocoder
from twython import TwythonStreamer
import string, json, pprint
import urllib
from datetime import datetime
from datetime import date
from time import *
import string, os, sys, subprocess, time
import psycopg2

# codes to access twitter API. 
APP_KEY = "Q530eYJ2divtkAltNRF9ORY6G"
APP_SECRET =  "xgRzCBf53goOm1ir06spIT8oAmvQFu5kr53ptycDn4CCEw0MYc"
OAUTH_TOKEN =  "2567730218-I3fdSSmhVi8vDq0zn94OGTnfkpTpPqKpOHaqvD5"
OAUTH_TOKEN_SECRET = "maoKC8LRS2rxpRmSz9mUbOCTc8TE2VxAaBJQTue2stqQS"

# Attempt to establish a connection to the database
try:
    con = psycopg2.connect("dbname=tweets user=user password=user" )
    cur = con.cursor()
except:
    print "Database connection error"           
   
# Class to process JSON data comming from the twitter stream API. Extract relevant fields
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        tweet_id = 9999999999
        tweet_text = "NaN"
        geo = None
        tweet_lon = 9999
        tweet_lat = 9999
        tweet_datetime = 9999
        tweet_name = "NaN"
        tweet_city = "NaN"
        tweet_lang = "NaN"
        retweet = 0
        tweet_source = "NaN"
        tweet_location = "NaN"
        tweet_countrycode = "NaN"
        tweet_countryname = "NaN"
        hyperlink = "NaN"
        
        if 'id' in data:
            tweet_id = data['id']
            
        if 'text' in data:
            tweet_text = data['text'].encode('utf-8').replace("'", '')
            if "https://t.co" in tweet_text:
                print True
            
        if 'coordinates' in data:    
            geo = data['coordinates']
            
        if not geo is None:
            latlon = geo['coordinates']
            tweet_lon = latlon[0]
            tweet_lat= latlon[1]
            
        if 'created_at' in data:
            dt = data['created_at']
            tweet_datetime = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
            
        if 'user' in data:
            users = data['user']
            if 'screen_name' in users and users['screen_name'] != None:
                tweet_name = users['screen_name'].encode('utf-8')
            if 'location' in users and users['location'] != None:
                tweet_city = users['location'].encode('utf-8')
            if 'lang' in users and users['lang'] != None:                
                tweet_lang = users['lang'].encode('utf-8')
            
        if 'source' in data:
            tweet_source = data['source'].encode('utf-8')
            
        if 'place' in data and data['place'] != None:
            place = data['place']
            if 'name' in place and place['name'] != None:
                tweet_location = place['name'].encode('utf-8')
            if 'country_code' in place and place['country_code'] != None:
                tweet_countrycode = place['country_code'].encode('utf-8')
            if 'country' in place and place['country'] != None:
                tweet_countryname = place['country'].encode('utf-8')         

        if tweet_location != "NaN" or tweet_countrycode != "NaN" or tweet_countryname != "NaN":
           
            # Compute coordinates from location and countryname
            g = geocoder.google('{}, {}'.format(tweet_location, tweet_countryname))
            outlatlon = g.latlng
            
            # Feed data to database defined in beginning of script
            insert_query = r"""
                            INSERT INTO public.drugtable VALUES(
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
            data = (str(tweet_id),
                    str(tweet_datetime),
                    str(tweet_lat),
                    str(tweet_lon),
                    str(tweet_city),
                    str(tweet_lang),
                    str(tweet_source),
                    str(tweet_countrycode),
                    str(tweet_countryname),
                    str(tweet_location),
                    str(hyperlink),
                    str(tweet_text),
                    outlatlon[0],
                    outlatlon[1])
            cur.execute(insert_query, data)
            con.commit()
            # print tweet_text
            
def main():
    try:
        stream = MyStreamer(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        print 'Connecting to twitter: will take a minute'
    except ValueError:
        con.close()
        cur.close()
        print 'Something went wrong while making connection with Twitter: '+str(ValueError)
    # Define what to track
    try:        
        stream.statuses.filter(track = ['alcohol,drugs,narcotics,cannabis,marijuana,ganja,xtc,mdma,cocaine,heroin,opium,amphetamines,methamfetamines,lsd'])
    except:
        cur.close
        con.close        
        print "Stream terminated"       
                
if __name__ == '__main__':
    main()