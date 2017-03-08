    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import psycopg2
import re
import geocoder
from twython import TwythonStreamer
import string, json, pprint
import urllib
from datetime import datetime
from datetime import date
import string, os, sys, subprocess, time

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
        outlatlon = [9999,9999]
        
        if 'id' in data:
            tweet_id = data['id']
            
        if 'text' in data:
            tweet_text = data['text'].encode('utf-8').replace("'", '')
            if "https://t.co" in tweet_text:
                all_hyperlinks = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet_text)
                hyperlink = all_hyperlinks[-1] # grab the last encountered URL, which to knowledge is the RT origin (needs testing!)
            
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

        if tweet_lon != 9999 or tweet_location != "NaN":
           
            # Compute coordinates from location and countryname
            if tweet_location != "NaN":
                g = geocoder.google('{}, {}'.format(tweet_location, tweet_countryname))
                outlatlon = g.latlng
            
            # Feed data to database defined in beginning of script
            """Table name must be entered manually in case another name is wanted
                If not, name is the same as specified in "createTable.py"""
            insert_query = r"INSERT INTO {}".format(tablename) + """ VALUES(
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
            data = (tweet_id,
                    str(tweet_datetime),
                    tweet_lat,
                    tweet_lon,
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
            cur.close
            con.close
            print hyperlink
            print tweet_text
            
def TweetsRealTime(dbname, user, password, table_name, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, loop_gathering = False, search_terms = ["Happy"]):
    """Using your own API keys, connects to the stream and starts gathering data"""
    try:
        """Be careful with the following global variables. They are necessary to make this script run from the main function
           This is because Twython streamer does not allow other inputs.
           If you run this script stand-alone you can safely remove the globals and it will still work."""
        global con 
        con = psycopg2.connect("dbname = {} user = {} password = {}".format(dbname,user,password))
        global cur
        cur = con.cursor()
        global tablename
        tablename = table_name
        print "Connected"
    except:
        print "Database connection error"    
    
    try:
        stream = MyStreamer(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        print 'Connecting to twitter: will take a minute'
    except ValueError:
        con.close()
        cur.close()
        print 'Something went wrong while making connection with Twitter: '+str(ValueError)

    try:
        stream.statuses.filter(track = search_terms)   
    except:
        # Shortcut to restarting the script - if the connection cancels then it gracefully terminates the db lock and establishes a new connection
        cur.close
        con.close        
        print "########### Stream terminated ###########"
        if loop_gathering != False:
            TweetsRealTime(dbname = dbname,
                                    user = user,
                                    password = password,
                                    table_name = table_name,
                                    search_terms = search_terms,
                                    APP_KEY = APP_KEY,
                                    APP_SECRET =  APP_SECRET,
                                    OAUTH_TOKEN =  OAUTH_TOKEN,
                                    OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRET,
                                    loop_gathering = loop_gathering)
        
if __name__ == '__main__':
    TweetsRealTime(dbname = "tweets",
                    user = "user",
                    password = "user",
                    table_name = "new",
                    APP_KEY = "",
                    APP_SECRET =  "",
                    OAUTH_TOKEN =  "",
                    OAUTH_TOKEN_SECRET = "",
                    loop_gathering = False,
                    search_terms = ["Happy"])