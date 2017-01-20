    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from twython import TwythonStreamer
import string, json, pprint
import urllib
from datetime import datetime
from datetime import date
from time import *
import string, os, sys, subprocess, time
import psycopg2

##codes to access twitter API. 
APP_KEY = "Q530eYJ2divtkAltNRF9ORY6G"
APP_SECRET =  "xgRzCBf53goOm1ir06spIT8oAmvQFu5kr53ptycDn4CCEw0MYc"
OAUTH_TOKEN =  "2567730218-I3fdSSmhVi8vDq0zn94OGTnfkpTpPqKpOHaqvD5"
OAUTH_TOKEN_SECRET = "maoKC8LRS2rxpRmSz9mUbOCTc8TE2VxAaBJQTue2stqQS"

##initiating Twython object 
#output_file = '/home/user/tweets/result_'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.csv' 

try:
    con = psycopg2.connect("dbname=tweets user=user password=user" )
    cur = con.cursor()
    print "the pentagon is hacked"
except:
    print "oops error"             
       
#Class to process JSON data comming from the twitter stream API. Extract relevant fields
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        tweet_lat = 0.0
        tweet_lon = 0.0
        tweet_name = ""
        retweet_count = 0

        if 'id' in data:
            tweet_id = data['id']
        else:
            tweet_id = 9999999999
            
        if 'text' in data:
            tweet_text = data['text'].encode('utf-8').replace("'", '')
        else:
            tweet_text = "NaN"
            
        if 'coordinates' in data:    
            geo = data['coordinates']
        else:
            geo = None
            
        if not geo is None:
            latlon = geo['coordinates']
            tweet_lon = latlon[0]
            tweet_lat= latlon[1]
        else:
            tweet_lon = 9999
            tweet_lat = 9999
            
        if 'created_at' in data:
            dt = data['created_at']
            tweet_datetime = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        if 'user' in data:
            users = data['user']
            tweet_name = users['screen_name']
            tweet_city = users['location']
            tweet_lang = users['lang']
        
        if 'retweet_count' in data:
            retweet = data['retweet_count']
        
        if 'source' in data:
            tweet_source = data['source']
        
        if 'place' in data:
            place = data['place']
            try:
                tweet_location = place['name']
            except:
                tweet_location = 9999
            try:
                tweet_countrycode = place['country_code']
            except:
                tweet_countrycode = 9999
            try:
                tweet_countryname = place['country']
            except:
                tweet_countryname = 9999 
            
        if 'source' in data:
            tweet_source = data['source'] if not data['source'] is None else "9999"

        #print string_to_write
        tweet_text.replace("'", '')
        try:
            insert_query = r"""
                INSERT INTO public.trumptweets VALUES(
                {id}, '{time}', '{latitude}', '{longitude}', '{city}', '{lang}', '{source}',
                '{countrycode}','{countryname}', '{location}', '{retweet}', '{text}')
                """.format( id = str(tweet_id),
                            time = str(tweet_datetime),
                            latitude = str(tweet_lat),
                            longitude = str(tweet_lon),
                            city = str(tweet_city),
                            lang = str(tweet_lang),
                            source = str(tweet_source),
                            countrycode = str(tweet_countrycode),
                            countryname = str(tweet_countryname),
                            location = str(tweet_location),
                            retweet = str(retweet),
                            text = str(tweet_text))     
            cur.execute(insert_query)
            con.commit()
        except:
            pass

#        i = 0
#        if i == 10:
#            cur.close()
#            con.close()

def main():
    try:
        stream = MyStreamer(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        print 'Connecting to twitter: will take a minute'
    except ValueError:
        print 'OOPS! that hurts, something went wrong while making connection with Twitter: '+str(ValueError)

    try:        
        stream.statuses.filter(track = ['trump'])
        #stream.statuses.filter(locations='-120.00,40.00,-70.35,63.65', )        
    except:
        runfile('/home/user/Desktop/gatherdata.py', wdir='/home/user/Desktop')  
        pass


#def write_tweet(t):
#    target = open(output_file, 'a')
#    target.write(t)
#    target.write('\n')
#    target.close()
                
if __name__ == '__main__':
    main()
