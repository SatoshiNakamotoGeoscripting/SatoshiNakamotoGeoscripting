#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 12:12:43 2017

@author: user
"""
import psycopg2
import json
from numpy import mean
import folium
import requests
import sys  
reload(sys) #Prevents errors with utf-8 encoding not working properly
sys.setdefaultencoding('utf8')

def getTweetsFromDB(dbname, user, password, table_name):
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, user, password))
    cursor = conn.cursor()
    
    # Retrieve data from database and extract coordinates
    cursor.execute("SELECT * FROM {} WHERE lang = 'en'".format(table_name))
    records = cursor.fetchall()
    
    list_of_tweets = []
    for i, record in enumerate(records):
        tweet_text = record[11].encode('utf-8')
        tweet_id = record[0]
        
        list_of_tweets.append([tweet_id,tweet_text])
    return list_of_tweets

tweets = getTweetsFromDB("tweets","user","user","trumptweets2")



def sentimentAnalyzer(tweets):
    #https://pypi.python.org/pypi/requests/
    #http://text-processing.com/docs/sentiment.html
    tweets_emotion = []
    i = 0
    #for i in range(10):
    for tweet in tweets:
        r = requests.post('http://text-processing.com/api/sentiment/', data = {'text': tweet[1]})
        ##https://market.mashape.com/japerk/text-processing/Pricing
        ## This API is limited to 45.000 requests per month (for free)
        tweet_id = tweet[0]
        tweet_id = str(tweet_id)
        tweet_id = int(tweet_id)
        emotion_prob = r.json()['probability']
        emotion_label = r.json()['label']
        emotion_prob = emotion_prob[emotion_label] #for only keeping the value corresponding to the label itself.
        tweets_emotion.append([tweet_id,emotion_prob,emotion_label])
        #print r.json()
        print(r.status_code, r.reason , i)
        i +=1
        #It takes 14 minutes for 2300 Tweets (165 per min or 3 per second)
    return tweets_emotion
tweets_emotion = sentimentAnalyzer(tweets)


## Should we 
def createTable(db_name, user, password, table_name, overwrite = False):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
        
    if overwrite == True:
        del_table_query = """DROP TABLE IF EXISTS {table_name};""".format(table_name = table_name)
        cur.execute(del_table_query)
    insert_query =  """CREATE TABLE IF NOT EXISTS {table_name} (
                        id  	bigint,
                        labelapi varchar(15),
                        sentimentapi numeric);
                    """.format(table_name = table_name)
    cur.execute(insert_query)
    con.commit()
    cur.close()
    con.close()

createTable(db_name="tweets", user="user", password="user", table_name = "sentiment_tweetsAPI", overwrite = True)
    

def insertSentiments(db_name, user, password, table_name, sentiment_tweets):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
    for tweet in sentiment_tweets:
        insert_query = r"""INSERT INTO public.sentiment_tweetsapi VALUES (%s,%s,%s)"""
        data = (tweet[0],tweet[2],tweet[1])
        cur.execute(insert_query, data)
    con.commit()
insertSentiments("tweets","user","user","sentiment_tweetsAPI",tweets_emotion)

def updateColumn(db_name, user, password,target_table,source_table, column_name, columntype):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
        
    drop_column = """
        ALTER TABLE trumptweets2 DROP COLUMN IF EXISTS {column_name};
    """.format(column_name = column_name)
    cur.execute(drop_column)
        
    add_column = """
        ALTER TABLE trumptweets2 ADD COLUMN {column_name}  {columntype};
    """.format(column_name=column_name, columntype =columntype)
    cur.execute(add_column)
    
    update = """
        UPDATE {target_table} t2
        SET    {column_name} = t1.{column_name}
        FROM   {source_table} t1
        WHERE  t2.id = t1.id              
    """.format(target_table=target_table,column_name=column_name,source_table=source_table)
    cur.execute(update)
    #AND    t2.val2 IS DISTINCT FROM t1.val1  -- optional, to avoid empty updates
    
    con.commit()
    
    
updateColumn("tweets", "user", "user","trumptweets2","sentiment_tweetsAPI","labelAPI","varchar(15)")
updateColumn("tweets", "user", "user","trumptweets2","sentiment_tweetsAPI","sentimentAPI","numeric")

