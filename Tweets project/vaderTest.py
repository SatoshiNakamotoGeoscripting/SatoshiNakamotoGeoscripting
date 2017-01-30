#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:23:07 2017

@author: user
"""
## FOUND HERE http://www.nltk.org/howto/sentiment.html
## Source code http://www.nltk.org/_modules/nltk/sentiment/vader.html
## http://www.nltk.org/api/nltk.sentiment.html
## Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model 
##for Sentiment Analysis of Social Media Text. Eighth International Conference on
## Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
## http://www.postgresqltutorial.com/postgresql-python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import psycopg2
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

def SentimentAnalyzer(tweets):
    sid = SentimentIntensityAnalyzer() #need to nltk.download() to use all the packages

    sentiment_tweets = []
    #for i in range(10):
    for tweet in tweets:   
        tweet_id = tweet[0]
        tweet_id = str(tweet_id)
        tweet_id = int(tweet_id)
        ss = sid.polarity_scores(tweet[1])
        if ss['compound'] <= -0.293:
            label = 'negative'
        elif ss['compound'] >= 0.293:
            label = 'positive'
        else:
            label = 'neutral'
        sentiment = ss['compound']
        
        sentiment_tweets.append((tweet_id,sentiment,label))
    return sentiment_tweets
                  
sentiment_tweets = SentimentAnalyzer(tweets)

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
                        label varchar(15),
                        sentiment numeric);
                    """.format(table_name = table_name)
    cur.execute(insert_query)
    con.commit()
    cur.close()
    con.close()
createTable(db_name="tweets", user="user", password="user", table_name = "sentiment_tweets", overwrite = True)

def insertSentiments(db_name, user, password, table_name, sentiment_tweets):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
    for tweet in sentiment_tweets:
        insert_query = r"""INSERT INTO public.sentiment_tweets VALUES (%s,%s,%s)"""
        data = (tweet[0],tweet[2],tweet[1])
        cur.execute(insert_query, data)
    con.commit()

insertSentiments("tweets","user","user","sentiment_tweets",sentiment_tweets)

#def joinTables(db_name, user, password):
#    try:
#        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
#        cur = con.cursor()
#    except:
#        print "oops error"
#        
#    drop_columns = """
#    ALTER TABLE trumptweets2 DROP COLUMN IF EXISTS sentiment;
#    ALTER TABLE trumptweets2 DROP COLUMN IF EXISTS label;
#    """
#    cur.execute(drop_columns)
#        
#    add_columns = """
#        ALTER TABLE trumptweets2 ADD COLUMN sentiment  decimal;
#        ALTER TABLE trumptweets2 ADD COLUMN label varchar(15);
#    """
#    cur.execute(add_columns)
#    
#    join = """
#        UPDATE public.trumptweets2 t1
#        JOIN sentiment_tweets t2 ON t1.id = t2.id 
#        SET t1.sentiment = t2.sentiment and t1.label = t2.label
#    """
#    cur.execute(join)
#    
#    con.commit()
#
#joinTables("tweets", "user", "user")
    
def insertintotables(db_name, user, password):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
    drop_columns = """
    ALTER TABLE trumptweets2 DROP COLUMN IF EXISTS sentiment;
    ALTER TABLE trumptweets2 DROP COLUMN IF EXISTS label;
    """
    cur.execute(drop_columns)
        
    add_columns = """
        ALTER TABLE trumptweets2 ADD COLUMN sentiment  decimal;
        ALTER TABLE trumptweets2 ADD COLUMN label varchar(15);
    """
    cur.execute(add_columns)
    
        
    insertinto = """INSERT INTO trumptweets2 (sentiment,label) 
                    SELECT sentiment_tweets.sentiment, sentiment_tweets.label 
                    FROM trumptweets2, sentiment_tweets 
                    WHERE sentiment_tweets.id = trumptweets2.id 
    """
    cur.execute(insertinto)
    con.commit()
insertintotables("tweets","user","user")